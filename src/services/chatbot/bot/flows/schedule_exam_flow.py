from typing import Union
from fastapi import HTTPException, Response, status
from src.services.chatbot.utils.date import convert_to_datetime, format_date_for_user, format_time_for_user, get_more_forty_five

from src.services.health_unit.models.repository.unidade_repository import UnidadeRepository
from src.services.schedules.exam.models.repository.exame_gendameno_repository import AgendamentoExameRepository

from src.log.logging import Logging
from src.services.user.models.repository.user_repository import UserRepository
from src.services.user_flow.models.repository.fluxo_etapa_repository import FluxoEtapaRepository
from src.services.health_agents.models.repository.especialidade_repository import EspecialidadeRepository



class ScheduleExamFlow:
    raise_message = "tente novamente ou entre em contato com o time de desenvolvimento através de chatsaude.al@gmail.com"

    def __init__(self, number: int, lang="br") -> None:
        self.lang = lang
        self.number = number

    async def initialize(self):
        self.user = await UserRepository().select_user_from_cellphone(self.number)
        if self.user.get('id') != None:
            self.user_flow = await FluxoEtapaRepository().select_stage_from_user_id(self.user['id'])


    async def load_unities(self):
        unities_entity = UnidadeRepository()
        unities = await unities_entity.select_all()
        unities_text = ""
        for i in unities:
            unities_text += f"""Unidade {i['id']}: {i['nome'].split('(')[0]}\nEndereço: {i['endereco'].replace(',','').split('s/n')[0]}\nBairro: {i['bairro']}\nHorario de funcionamento: {i['horario_funcionamento']}\n"""
        return unities_text

    async def get_last_time_schedule(self) -> str:
        exam_entity = AgendamentoExameRepository()
        data_schedule = (
            await exam_entity.select_data_schedule_from_user_cellphone(
                int(self.user["telefone"])
            )
        )
        last_time = None
        if data_schedule["id_especialidade"] is not None and data_schedule["id_unidade"] is not None:
            last_time = (
                await exam_entity.get_last_time_scheduele_from_specialty_id(
                    int(data_schedule["id_especialidade"]),
                    int(data_schedule["id_unidade"]),
                )
            )
        if last_time is not None and data_schedule["id_unidade"] is not None:
            data = await format_date_for_user(last_time["data_agendamento"])
            hora = await format_time_for_user(
                last_time["horario_termino_agendamento"]
            )
            return f"""Digite o dia que você deseja realizar a exama\nEx: 24/12/2023\nAtenção, para essa especialidade somente temos horários a partir do dia {data}, a partir das {hora}"""
        else:
            return """Digite o dia que você deseja realizar a exama\nEx: 24/12/2023"""


    async def check_conflict(self, message) -> dict[str, bool]:
        exam_entity = AgendamentoExameRepository()
        data_schedule = (
            await exam_entity.select_data_schedule_from_user_cellphone(
                int(self.user["telefone"])
            )
        )
        if data_schedule['horario_inicio_agendamento'] != None:
            conflict = await exam_entity.check_conflicting_schedule(
                data_schedule["id_unidade"],
                data_schedule["id_especialidade"],
                data_schedule["data_agendamento"],
                str(message) + ":00",
                await get_more_forty_five(message),
                data_schedule["id"],
            )
            return {'value': True, 'content': message} if not conflict else {'value': False, 'content': None}

        return {'value': True, 'content': message}


    async def init_exam_flow(self) -> bool:
        flow_entity = FluxoEtapaRepository()
        schedule_exam_entity = AgendamentoExameRepository()
        await flow_entity.update_flow_from_user_id(
            self.user["id"], "etapa_agendamento_exame", 1
        )
        await schedule_exam_entity.insert_new_schedule_exam(self.user["id"]),
        return True

    async def define_specialty_exam(self, message: str) -> Union[str, HTTPException]:
        """
        Método responsável por definir a especialidade da con-
        sulta do usuário
          :params user: dict
          :params message: string
          :params flow_status: int
        """
        exam_entity = AgendamentoExameRepository()
        flow_entity = FluxoEtapaRepository()
        specialty_entity = EspecialidadeRepository()
        flow_status = self.user_flow["etapa_agendamento_exame"] + 1

        try:
            schedule_data = await exam_entity.select_data_schedule_from_user_id(self.user["id"])
            specialty_user_request = (
                await specialty_entity.select_specialty_from_name(message)
            )
            await flow_entity.update_flow_from_user_id(
                self.user["id"], "etapa_agendamento_exame", flow_status
            )
            response = await exam_entity.update_schedule_from_id(
                schedule_data["id"],
                "id_especialidade",
                specialty_user_request["id"],
            )
            return response

        except Exception as error:
            message_log = "Erro ao definir a especialidade do exame no banco de dados"
            log = Logging(message_log)
            await log.warning(
                "define_specialty_exam",
                None,
                str(error),
                500,
                {"params": {"message": message, "user": self.user, 'flow_status': flow_status}},
            )
            raise_message = raise_message =  f"Desculpe, não foi possível definir o exame solicitado, {ScheduleExamFlow.raise_message}"
            return {'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR, 'detail': raise_message}

    async def define_unity_exam(self, message: str) -> Union[str, HTTPException]:
        """
        Método responsável por definir unidade da exama do
        usuário no banco de dados
          :params user: dict
          :params message: string
          :params flow_status: int
        """
        exam_entity = AgendamentoExameRepository()
        flow_entity = FluxoEtapaRepository()
        specialty_entity = EspecialidadeRepository()
        flow_status = self.user_flow["etapa_agendamento_exame"] + 1

        try:
            schedule_data = await exam_entity.select_data_schedule_from_user_id(self.user["id"])
            await flow_entity.update_flow_from_user_id(
                self.user["id"], "etapa_agendamento_exame", flow_status
            )
            await exam_entity.update_schedule_from_id(
                schedule_data["id"], "id_unidade", int(message)
            )
            return True

        except Exception as error:
            message_log = "Erro ao registrar a unidade do exame no banco de dados"
            log = Logging(message_log)
            await log.warning(
                "define_unity_exam",
                None,
                str(error),
                500,
                {"params": {"message": message, "user": self.user, 'flow_status': flow_status}},
            )
            raise_message = f"Desculpe, não foi possível registrar adequadamente a unidade solicitada, {ScheduleExamFlow.raise_message}"
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=raise_message
            )

    async def define_date_exam(self, date: str) -> Union[str, HTTPException]:
        """
        Método responsável por definir a data da exama do
        usuário no banco de dados
          :params user: dict
          :params message: string
          :params flow_status: int
        """
        exam_entity = AgendamentoExameRepository()
        flow_entity = FluxoEtapaRepository()
        specialty_entity = EspecialidadeRepository()
        flow_status = self.user_flow["etapa_agendamento_exame"] + 1

        try:
            schedule_data = await exam_entity.select_data_schedule_from_user_id(self.user["id"])
            await flow_entity.update_flow_from_user_id(
                self.user["id"], "etapa_agendamento_exame", flow_status
            )
            await exam_entity.update_schedule_from_id(
                schedule_data["id"], "data_agendamento", date
            )
            return True

        except Exception as error:
            message_log = "Erro ao registrar a data do exame no banco de dados"
            log = Logging(message_log)
            await log.warning(
                "define_date_exam",
                None,
                str(error),
                500,
                {"params": {"date": date, "user": self.user, 'flow_status': flow_status}},
            )
            raise_message = f"Desculpe, não foi possível registrar adequadamente a data solicitada, {ScheduleExamFlow.raise_message}"
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=raise_message
            )

    async def define_time_exam(self, message: str) -> Union[str, HTTPException]:
        """
        Método responsável por definir hora da exama do
        usuário no banco de dados
            :params user: dict
            :params message: string
            :params flow_status: int
        """
        exam_entity = AgendamentoExameRepository()
        flow_entity = FluxoEtapaRepository()
        specialty_entity = EspecialidadeRepository()
        flow_status = self.user_flow["etapa_agendamento_exame"] + 1

        try:
            schedule_data = await exam_entity.select_data_schedule_from_user_id(self.user["id"])
            await flow_entity.update_flow_from_user_id(
                self.user["id"], "etapa_agendamento_exame", flow_status
            )
            final_schedule = await get_more_forty_five(str(message))
            exam_data = await exam_entity.update_schedule_from_id(
                schedule_data["id"],
                "horario_inicio_agendamento",
                await convert_to_datetime(str(message) + ":00"),
            )
            await exam_entity.update_schedule_from_id(
                schedule_data["id"],
                "horario_termino_agendamento",
                await convert_to_datetime(final_schedule),
            )
            return True

        except Exception as error:
            message_log = "Erro ao registrar a hora do exame no banco de dados"
            log = Logging(message_log)
            await log.warning(
                "define_time_exam",
                None,
                str(error),
                500,
                {"params": {"message": message, "user": self.user, 'flow_status': flow_status}},
            )
            raise_message = f"Desculpe, não foi possível definir a hora do exame, {ScheduleExamFlow.raise_message}"
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=raise_message
            )

    async def define_necessity_exam(self, message: str) -> Union[str, HTTPException]:
        """
        Método responsável por definir a necessidade da
        exama do usuário no banco de dados
            :params user: dict
            :params message: string
            :params flow_status: int
        """
        exam_entity = AgendamentoExameRepository()
        flow_entity = FluxoEtapaRepository()
        try:
            schedule_data = await exam_entity.select_data_schedule_from_user_id(self.user["id"])
            await flow_entity.update_flow_from_user_id(
                self.user["id"], "etapa_agendamento_exame", 0
            )
            await flow_entity.update_flow_from_user_id(
                self.user["id"], "fluxo_agendamento_exame", 0
            )
            return True

        except Exception as error:
            message_log = "Erro ao registrar a necessidade do usuário no banco de dados!"
            log = Logging(message_log)
            await log.warning(
                "define_necessity_exam",
                None,
                str(error),
                500,
                {"params": {"message": message, "user": self.user}},
            )
            raise_message = f"Desculpe, não conseguimos definir a necessidade da sua consulta, {ScheduleExamFlow.raise_message}"
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message_log
            )

    async def finalize_schedule_flow(self) -> Union[str, HTTPException]:
        """
        Método responsável por finalizar o fluxo de agendamento
            :params user: dict
            :params message: string
            :params flow_status: int
        """
        exam_entity = AgendamentoExameRepository()
        flow_entity = FluxoEtapaRepository()
        try:
            schedule_data = await exam_entity.select_data_schedule_from_user_id(self.user["id"])
            await flow_entity.update_flow_from_user_id(
                self.user["id"], "etapa_agendamento_exame", 0
            )
            await flow_entity.update_flow_from_user_id(
                self.user["id"], "fluxo_agendamento_exame", 0
            )
            all_data = await exam_entity.select_all_data_from_schedule_with_id(
                schedule_data["id"]
            )
            content = f"Que ótimo, você realizou seu agendamento!\nCompareça à unidade {all_data['unity_info']['nome']} no dia {await format_date_for_user(all_data['data_agendamento'])} as {await format_time_for_user(all_data['horario_inicio_agendamento'])} horas para a sua exama com o {all_data['specialty_info']['nome']}"
            return content

        except Exception as error:
            message_log = "Erro ao finalizar o fluxo de agendamento de exame"
            log = Logging(message_log)
            await log.warning(
                "finalize_schedule_flow",
                None,
                str(error),
                500,
                {"params": {"user": self.user}},
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message_log
            )
