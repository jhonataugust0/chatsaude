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

    # async def data_schedule_consult_update_flow(self, user: dict, message: str):
    #     unities_entity = UnidadeRepository()
    #     consult_entity = AgendamentoConsultaRepository()
    #     flow_entity = FluxoEtapaRepository()
    #     number_formated = f"whatsapp:+" + str(user["telefone"])
    #     register_consult_flow = ScheduleConsultFlow()

    #     async def send_success_message(content: str):
    #         await send_message(content, number_formated)
    #         return Response(
    #             status_code=status.HTTP_200_OK, content="Mensagem enviada com sucesso"
    #         )

    #     async def send_error_message(reply: str):
    #         await send_message(reply, number_formated)
    #         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=reply)

    #     try:
    #         user_flow = await flow_entity.select_stage_from_user_id(int(user["id"]))
    #         flow_status = user_flow["etapa_agendamento_consulta"] + 1
    #         number_formated = f"whatsapp:+" + str(user["telefone"])
    #         schedule_data = await consult_entity.select_data_schedule_from_user_id(
    #             user["id"]
    #         )

    #         if user_flow["etapa_agendamento_consulta"] == 1:
    #             await register_consult_flow.define_specialty_consult(
    #                 user, message, flow_status
    #             )
    #             await send_success_message(
    #                 "Escolha a unidade suportada mais próxima de você\nDigite o número correspondente ao da unidade desejada\nEx: 1"
    #             )

    #             unities = await unities_entity.select_all()
    #             for i in unities:
    #                 unities_text = f"""Unidade {i['id']}: {i['nome'].split('(')[0]}\nEndereço: {i['endereco'].replace(',','').split('s/n')[0]}\nBairro: {i['bairro']}\nHorario de funcionamento: {i['horario_funcionamento']}"""
    #                 await send_message(unities_text, number_formated)

    #             return Response(
    #                 status_code=status.HTTP_200_OK,
    #                 content="Mensagem enviada com sucesso",
    #             )

    #         elif user_flow["etapa_agendamento_consulta"] == 2:
    #             consult_data = await register_consult_flow.define_unity_consult(
    #                 user, int(message), flow_status
    #             )
    #             last_time = (
    #                 await consult_entity.get_last_time_scheduele_from_specialty_id(
    #                     int(consult_data["id_especialidade"]),
    #                     int(consult_data["id_unidade"]),
    #                 )
    #             )

    #             if consult_data["id_unidade"] and last_time:
    #                 data = await format_date_for_user(last_time[-1]["data_agendamento"])
    #                 hora = await format_time_for_user(
    #                     last_time[-1]["horario_termino_agendamento"]
    #                 )
    #                 await send_message(
    #                     f"""Digite o dia que você deseja realizar a consulta\nEx: 24/12/2023\nAtenção, para essa especialidade somente temos horários a partir do dia {data}, a partir das {hora}""",
    #                     number_formated,
    #                 )
    #             else:
    #                 await send_message(
    #                     f"""Digite o dia que você deseja realizar a consulta\nEx: 24/12/2023""",
    #                     number_formated,
    #                 )

    #             return Response(
    #                 status_code=status.HTTP_200_OK,
    #                 content="Mensagem enviada com sucesso",
    #             )

            # elif user_flow["etapa_agendamento_consulta"] == 3:
            #     date = await Input_validator.validate_date_schedule(message)
            #     if date["value"]:
            #         await register_consult_flow.define_date_consult(
            #             user, date["date"], flow_status
            #         )
            #         await send_message(
            #             "Digite o horário que deseja realizar a consulta (atente-se para o horário estar dentro do período de funcionamento da unidade escolhida)\nEx: 08:00",
            #             number_formated,
            #         )
            #     else:
            #         reply = "Por favor, digite uma data válida"
            #         await send_error_message(reply)

            #     return Response(
            #         status_code=status.HTTP_200_OK,
            #         content="Mensagem enviada com sucesso",
            #     )

            # elif user_flow["etapa_agendamento_consulta"] == 4:
            #     data_schedule = (
            #         await consult_entity.select_data_schedule_from_user_cellphone(
            #             int(user["telefone"])
            #         )
            #     )
            #     conflict = await consult_entity.check_conflicting_schedule(
            #         data_schedule["id_unidade"],
            #         data_schedule["id_especialidade"],
            #         data_schedule["data_agendamento"],
            #         str(message) + ":00",
            #         await get_more_forty_five(message),
            #         data_schedule["id"],
            #     )

            #     if conflict:
            #         await send_message(
            #             "Desculpe, esse horário está indisponível, por favor, informe um horário no mínimo superior ao informado anteriormente",
            #             number_formated,
            #         )
            #     else:
            #         await register_consult_flow.define_time_consult(
            #             user, message, flow_status
            #         )
            #         await send_message(
            #             "(Opcional) Digite uma mensagem descrevendo qual a sua necessidade para a especialidade escolhida.\nEx: Exame de rotina\nVocê pode digitar qualquer coisa para ignorar essa etapa)",
            #             number_formated,
            #         )

                # return Response(
                #     status_code=status.HTTP_200_OK,
                #     content="Mensagem enviada com sucesso",
                # )

    #         elif user_flow["etapa_agendamento_consulta"] == 5:
    #             await register_consult_flow.define_necessity_consult(
    #                 user, message, flow_status
    #             )
    #             all_data = await register_consult_flow.finalize_schedule_flow(
    #                 user, message, flow_status
    #             )

    #             content = f"Que ótimo, você realizou seu agendamento!\nCompareça à unidade {all_data['unity_info']['nome']} no dia {await format_date_for_user(all_data['data_agendamento'])} as {await format_time_for_user(all_data['horario_inicio_agendamento'])} horas para a sua consulta com o {all_data['specialty_info']['nome']}"
    #             return await send_success_message(content)

    #         if (
    #             user_flow["etapa_agendamento_consulta"] == 0
    #             or user_flow["etapa_agendamento_consulta"] == 0
    #         ):
    #             consult_flow_stage = await flow_entity.update_flow_from_user_id(
    #                 user["id"], "etapa_agendamento_consulta", 1
    #             )
    #             return Response(
    #                 status_code=status.HTTP_200_OK,
    #                 content="Fluxo atualizado com sucesso",
    #             )

    #     except Exception as error:
    #         message_log = "Erro ao atualizar os dados do agendamento no banco de dados"
    #         log = Logging(message_log)
    #         await log.warning(
    #             "data_schedule_consult_update_flow",
    #             None,
    #             str(error),
    #             500,
    #             {"params": {"message": message, "user": user}},
    #         )
    #         raise HTTPException(
    #             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message_log
    #         )

    async def data_schedule_exam_update_flow(self, user: dict, message: str):
        unities_entity = UnidadeRepository()
        exam_entity = AgendamentoExameRepository()
        flow_entity = FluxoEtapaRepository()
        number_formated = f"whatsapp:+" + str(user["telefone"])
        register_consult_flow = ScheduleExamFlow()

        async def send_success_message(content: str):
            await send_message(content, number_formated)
            return Response(
                status_code=status.HTTP_200_OK, content="Mensagem enviada com sucesso"
            )

        async def send_error_message(reply: str):
            await send_message(reply, number_formated)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=reply)

        try:
            user_flow = await flow_entity.select_stage_from_user_id(int(user["id"]))
            flow_status = user_flow["etapa_agendamento_exame"] + 1
            number_formated = f"whatsapp:+" + str(user["telefone"])
            schedule_data = await exam_entity.select_data_schedule_from_user_id(
                user["id"]
            )

            if user_flow["etapa_agendamento_exame"] == 1:
                await register_consult_flow.define_specialty_consult(
                    user, message, flow_status
                )
                await send_success_message(
                    "Escolha a unidade suportada mais próxima de você\nDigite o número correspondente ao da unidade desejada\nEx: 1"
                )

                unities = await unities_entity.select_all()
                for i in unities:
                    unities_text = f"""Unidade {i['id']}: {i['nome'].split('(')[0]}\nEndereço: {i['endereco'].replace(',','').split('s/n')[0]}\nBairro: {i['bairro']}\nHorario de funcionamento: {i['horario_funcionamento']}"""
                    await send_message(unities_text, number_formated)

                return Response(
                    status_code=status.HTTP_200_OK, content="Mensagem enviada com sucesso"
                )

            elif user_flow["etapa_agendamento_exame"] == 2:
                consult_data = await register_consult_flow.define_unity_consult(
                    user, int(message), flow_status
                )
                last_time = await exam_entity.get_last_time_scheduele_from_specialty_id(
                    int(consult_data["id_especialidade"]),
                    int(consult_data["id_unidade"]),
                )

                if consult_data["id_unidade"] and last_time:
                    data = await format_date_for_user(last_time[-1]["data_agendamento"])
                    hora = await format_time_for_user(
                        last_time[-1]["horario_termino_agendamento"]
                    )
                    await send_message(
                        f"""Digite o dia que você deseja realizar a consulta\nEx: 24/12/2023\nAtenção, para essa especialidade somente temos horários a partir do dia {data}, a partir das {hora}""",
                        number_formated,
                    )
                else:
                    await send_message(
                        f"""Digite o dia que você deseja realizar a consulta\nEx: 24/12/2023""",
                        number_formated,
                    )

                return Response(
                    status_code=status.HTTP_200_OK, content="Mensagem enviada com sucesso"
                )

            elif user_flow["etapa_agendamento_exame"] == 3:
                date = await Input_validator.validate_date_schedule(message)
                if date["value"]:
                    await register_consult_flow.define_date_consult(
                        user, date["date"], flow_status
                    )
                    await send_message(
                        "Digite o horário que deseja realizar a consulta (atente-se para o horário estar dentro do período de funcionamento da unidade escolhida)\nEx: 08:00",
                        number_formated,
                    )
                else:
                    reply = "Por favor, digite uma data válida"
                    await send_error_message(reply)

            elif user_flow["etapa_agendamento_exame"] == 4:
                data_schedule = (
                    await exam_entity.select_data_schedule_from_user_cellphone(
                        int(user["telefone"])
                    )
                )
                conflict = await exam_entity.check_conflicting_schedule(
                    data_schedule["id_unidade"],
                    data_schedule["id_especialidade"],
                    data_schedule["data_agendamento"],
                    str(message) + ":00",
                    await get_more_forty_five(message),
                    data_schedule["id"],
                )

                if conflict:
                    await send_message(
                        "Desculpe, esse horário está indisponível, por favor, informe um horário no mínimo superior ao informado anteriormente",
                        number_formated,
                    )
                else:
                    await register_consult_flow.define_time_consult(
                        user, message, flow_status
                    )
                    await send_message(
                        "(Opcional) Digite uma mensagem descrevendo qual a sua necessidade para a especialidade escolhida.\nEx: Exame de rotina\nVocê pode digitar qualquer coisa para ignorar essa etapa)",
                        number_formated,
                    )

                return Response(
                    status_code=status.HTTP_200_OK, content="Mensagem enviada com sucesso"
                )

            elif user_flow["etapa_agendamento_exame"] == 5:
                await register_consult_flow.define_necessity_consult(
                    user, message, flow_status
                )
                all_data = await register_consult_flow.finalize_schedule_flow(
                    user, message, flow_status
                )

                content = f"Que ótimo, você realizou seu agendamento!\nCompareça à unidade {all_data['unity_info']['nome']} no dia {await format_date_for_user(all_data['data_agendamento'])} as {await format_time_for_user(all_data['horario_inicio_agendamento'])} horas para a sua consulta com o {all_data['specialty_info']['nome']}"
                return await send_success_message(content)

            if user_flow["etapa_agendamento_exame"] == 0:
                consult_flow_stage = await flow_entity.update_flow_from_user_id(
                    user["id"], "etapa_agendamento_exame", 1
                )
                return await send_success_message("Fluxo atualizado com sucesso")

        except Exception as error:
            message_log = "Erro ao atualizar os dados do agendamento no banco de dados"
            log = Logging(message_log)
            await log.warning(
                "data_schedule_consult_update_flow",
                None,
                str(error),
                500,
                {"params": {"message": message, "user": user}},
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message_log
            )
