from time import sleep
from ..bot.replies import Replies
from api.log.logging import Logging
from datetime import time as time_type
from datetime import date as date_type
from ..bot.Bot_options import BotOptions
from fastapi import HTTPException, Response, status
from ..bot.flows.register_user_flow import RegisterUserFlow
from ..bot.flows.schedule_consult_flow import ScheduleConsultFlow
from ..bot.flows.schedule_exam_flow import ScheduleExamFlow

from ...schedules.consult.models.repository.consulta_agendameno_repository import (
    AgendamentoConsultaRepository,
)
from ...schedules.exam.models.repository.exame_gendameno_repository import (
    AgendamentoExameRepository,
)
from api.services.user_flow.models.repository.fluxo_etapa_repository import (
    FluxoEtapaRepository,
)
from api.services.health_unit.models.repository.unidade_repository import (
    UnidadeRepository,
)
from api.services.user.models.repository.user_repository import UserRepository
from ..utils.bot_utils import send_message

from .triggers.register_user_trigger import RegisterUserTrigger
from .triggers.schedule_consult_triggers import ScheduleConsultTrigger
from .triggers.schedule_exam_triggers import ScheduleExamTrigger
from .triggers.make_report_trigger import MakeReportTrigger

from .validators.document_validator import Document_validator
from .validators.input_validator import Input_validator

from ..utils.date import (
    convert_to_datetime,
    format_date_for_user,
    format_time_for_user,
    get_more_forty_five,
)


class BotDispatcher:
    def __init__(self, lang="br") -> None:
        self.lang = lang

    async def message_processor(
        self, message: str, cellphone: int, user_dict: dict = None
    ) -> dict[str]:
        """
        Método que processa as inputs do usuário, identificando-as e atribuindo as
        mesmas seus respectivos gatilhos para a continuidade do fluxo da aplicação.
        :params message: str
        :params cellphone: int
        return dict | Response: Response
        """
        try:
            if user_dict is not None and user_dict.get("telefone") is not None:
                flow_entity = FluxoEtapaRepository()
                verify_stage_user = await flow_entity.select_stage_from_user_id(
                    user_dict["id"]
                )

                if message == BotOptions.SCHEDULE_CONSULT:
                    response = await ScheduleConsultTrigger.schedule_consult_trigger(
                        verify_stage_user, cellphone
                    )

                elif message == BotOptions.SCHEDULE_EXAM:
                    response = await ScheduleExamTrigger.schedule_exam_trigger(
                        verify_stage_user, cellphone
                    )

                elif message == BotOptions.MAKE_REPORT:
                    response = await MakeReportTrigger.make_report_trigger()

                else:
                    response = await Replies.default_reply(verify_stage_user)

            elif message == BotOptions.REGISTER_USER:
                response = await RegisterUserTrigger.register_user_trigger(user_dict, cellphone)

            else:
                response = await Replies.default_new_user_reply(user_dict)

            return response

        except Exception as error:
            message_log = f"Erro ao processar a input do usuário {message}"
            log = Logging(message_log)
            await log.warning(
                "message_processor",
                None,
                str(error),
                500,
                {"params": {"message": message, "cellphone": cellphone}},
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message_log
            )

    async def trigger_processing(
        self, bot_response: dict, number: int, user: dict = None
    ) -> Response:
        try:
            user_entity = UserRepository()
            register_flow = RegisterUserFlow()
            stage_entity = FluxoEtapaRepository()
            schedule_consult_entity = AgendamentoConsultaRepository()
            schedule_exam_entity = AgendamentoExameRepository()

            trigger_actions = {
                "register_user_trigger": {
                    "action": [lambda: register_flow.insert_user_and_flow(number)],
                    "message": "Usuário inserido com sucesso",
                },
                "schedule_consult_trigger": {
                    "action": [
                        lambda: stage_entity.update_flow_from_user_id(
                            user["id"], "fluxo_agendamento_consulta", 1
                        ),
                        lambda: stage_entity.update_flow_from_user_id(
                            user["id"], "etapa_agendamento_consulta", 0
                        ),
                        lambda: schedule_consult_entity.insert_new_schedule_consult(
                            user["id"]
                        ),
                    ],
                    "message": "Agendamento de consulta iniciado com sucesso",
                },
                "schedule_exam_trigger": {
                    "action": [
                        lambda: stage_entity.update_flow_from_user_id(
                            user["id"], "fluxo_agendamento_exame", 1
                        ),
                        lambda: stage_entity.update_flow_from_user_id(
                            user["id"], "etapa_agendamento_exame", 0
                        ),
                        lambda: schedule_exam_entity.insert_new_schedule_exam(
                            user["id"]
                        ),
                    ],
                    "message": "Agendamento de exame iniciado com sucesso",
                },
                # "make_report_trigger": {
                #     "action": lambda: await schedule_consult_entity.make_report(user, report_entity),
                #     "message": "Relatório gerado com sucesso",
                # },
            }

            if bot_response is not None:
                for trigger in bot_response:
                    if trigger in trigger_actions and bot_response[trigger] == 1:
                        for func in trigger_actions[trigger]["action"]:
                            await func()

                        return Response(
                            status_code=status.HTTP_200_OK,
                            content=trigger_actions[trigger]["message"],
                        )

        except Exception as error:
            message_log = f"Erro ao processar os gatilhos {bot_response}"
            log = Logging(message_log)
            await log.warning(
                "trigger_processing",
                None,
                str(error),
                500,
                {"params": {"number": number, "bot_response": bot_response}},
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message_log
            )

