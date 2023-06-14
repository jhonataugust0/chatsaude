from fastapi import HTTPException, Response, status
from api.services.chatbot.utils.date import convert_to_datetime, get_more_forty_five

from api.services.health_unit.models.repository.unidade_repository import UnidadeRepository
from api.services.schedules.exam.models.repository.exame_gendameno_repository import AgendamentoExameRepository

from .....log.logging import Logging
from ...utils.bot_utils import send_message
from api.services.user.models.repository.user_repository import UserRepository
from api.services.user_flow.models.repository.fluxo_etapa_repository import FluxoEtapaRepository
from api.services.health_agents.models.repository.especialidade_repository import EspecialidadeRepository



class ScheduleExamFlow:
    def __init__(self, lang="br") -> None:
        self.lang = lang

    async def define_specialty_consult(self, user: dict, message: str, flow_status: int) -> Response | HTTPException:
        """
        Método responsável por definir a especialidade da con-
        sulta do usuário
          :params user: dict
          :params message: string
          :params flow_status: int
        """
        consult_entity = AgendamentoExameRepository()
        flow_entity = FluxoEtapaRepository()
        specialty_entity = EspecialidadeRepository()

        try:
            schedule_data = await consult_entity.select_data_schedule_from_user_id(user["id"])
            specialty_user_request = (
                await specialty_entity.select_specialty_from_name(message)
            )
            await flow_entity.update_flow_from_user_id(
                user["id"], "etapa_agendamento_exame", flow_status
            )
            consult_data = await consult_entity.update_schedule_from_id(
                schedule_data["id"],
                "id_especialidade",
                specialty_user_request["id"],
            )
            return consult_data

        except Exception as error:
            message_log = "Erro ao definir a especialidade da consulta no banco de dados"
            log = Logging(message_log)
            await log.warning(
                "define_specialty_consult",
                None,
                str(error),
                500,
                {"params": {"message": message, "user": user, 'flow_status': flow_status}},
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message_log
            )

    async def define_unity_consult(self, user: dict, message: str, flow_status: int) -> Response | HTTPException:
        """
        Método responsável por definir unidade da consulta do
        usuário no banco de dados
          :params user: dict
          :params message: string
          :params flow_status: int
        """
        consult_entity = AgendamentoExameRepository()
        flow_entity = FluxoEtapaRepository()
        specialty_entity = EspecialidadeRepository()

        try:
            schedule_data = await consult_entity.select_data_schedule_from_user_id(user["id"])
            user_flow = await flow_entity.update_flow_from_user_id(
                user["id"], "etapa_agendamento_exame", flow_status
            )
            consult_data = await consult_entity.update_schedule_from_id(
                schedule_data["id"], "id_unidade", message
            )
            return consult_data

        except Exception as error:
            message_log = "Erro ao registrar a unidade da consulta no banco de dados"
            log = Logging(message_log)
            await log.warning(
                "define_unity_consult",
                None,
                str(error),
                500,
                {"params": {"message": message, "user": user, 'flow_status': flow_status}},
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message_log
            )

    async def define_date_consult(self, user: dict, date: str, flow_status: int) -> Response | HTTPException:
        """
        Método responsável por definir a data da consulta do
        usuário no banco de dados
          :params user: dict
          :params message: string
          :params flow_status: int
        """
        consult_entity = AgendamentoExameRepository()
        flow_entity = FluxoEtapaRepository()
        specialty_entity = EspecialidadeRepository()

        try:
            schedule_data = await consult_entity.select_data_schedule_from_user_id(user["id"])
            user_flow = await flow_entity.update_flow_from_user_id(
                user["id"], "etapa_agendamento_exame", flow_status
            )
            await consult_entity.update_schedule_from_id(
                schedule_data["id"], "data_agendamento", date
            )
            return Response(
                status_code=status.HTTP_200_OK,
                content="Data registrada com sucesso",
            )

        except Exception as error:
            message_log = "Erro ao registrar a data da consulta no banco de dados"
            log = Logging(message_log)
            await log.warning(
                "define_date_consult",
                None,
                str(error),
                500,
                {"params": {"date": date, "user": user, 'flow_status': flow_status}},
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message_log
            )

    async def define_time_consult(self, user: dict, message: str, flow_status: int) -> Response | HTTPException:
        """
        Método responsável por definir hora da consulta do
        usuário no banco de dados
            :params user: dict
            :params message: string
            :params flow_status: int
        """
        consult_entity = AgendamentoExameRepository()
        flow_entity = FluxoEtapaRepository()
        specialty_entity = EspecialidadeRepository()
        try:
            schedule_data = await consult_entity.select_data_schedule_from_user_id(user["id"])
            user_flow = await flow_entity.update_flow_from_user_id(
                user["id"], "etapa_agendamento_exame", flow_status
            )
            final_schedule = await get_more_forty_five(str(message))
            consult_data = await consult_entity.update_schedule_from_id(
                schedule_data["id"],
                "horario_inicio_agendamento",
                await convert_to_datetime(str(message) + ":00"),
            )
            consult_data = await consult_entity.update_schedule_from_id(
                schedule_data["id"],
                "horario_termino_agendamento",
                await convert_to_datetime(final_schedule),
            )
            return consult_data

        except Exception as error:
            message_log = "Erro ao registrar a hora da consulta no banco de dados"
            log = Logging(message_log)
            await log.warning(
                "define_time_consult",
                None,
                str(error),
                500,
                {"params": {"message": message, "user": user, 'flow_status': flow_status}},
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message_log
            )

    async def define_necessity_consult(self, user: dict, message: str, flow_status: int) -> Response | HTTPException:
        """
        Método responsável por definir a necessidade da
        consulta do usuário no banco de dados
            :params user: dict
            :params message: string
            :params flow_status: int
        """
        consult_entity = AgendamentoExameRepository()
        flow_entity = FluxoEtapaRepository()
        try:
            schedule_data = await consult_entity.select_data_schedule_from_user_id(user["id"])
            await flow_entity.update_flow_from_user_id(
                user["id"], "etapa_agendamento_exame", 0
            )
            await flow_entity.update_flow_from_user_id(
                user["id"], "fluxo_agendamento_exame", 0
            )
            consult_data = await consult_entity.update_schedule_from_id(
                schedule_data["id"], "descricao_necessidade", str(message)
            )
            consult_data

        except Exception as error:
            message_log = "Erro ao registrar a necessidade do usuário no banco de dados!"
            log = Logging(message_log)
            await log.warning(
                "define_necessity_consult",
                None,
                str(error),
                500,
                {"params": {"message": message, "user": user}},
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message_log
            )

    async def finalize_schedule_flow(self, user: dict, message: str, flow_status: int) -> Response | HTTPException:
        """
        Método responsável por finalizar o fluxo de agendamento
            :params user: dict
            :params message: string
            :params flow_status: int
        """
        consult_entity = AgendamentoExameRepository()
        flow_entity = FluxoEtapaRepository()
        try:
            schedule_data = await consult_entity.select_data_schedule_from_user_id(user["id"])
            await flow_entity.update_flow_from_user_id(
                user["id"], "etapa_agendamento_exame", 0
            )
            await flow_entity.update_flow_from_user_id(
                user["id"], "fluxo_agendamento_consulta", 0
            )
            all_data = await consult_entity.select_all_data_from_schedule_with_id(
                schedule_data["id"]
            )
            return all_data

        except Exception as error:
            message_log = "Erro ao finalizar o fluxo de agendamento de consulta"
            log = Logging(message_log)
            await log.warning(
                "finalize_schedule_flow",
                None,
                str(error),
                500,
                {"params": {"message": message, "user": user}},
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message_log
            )
