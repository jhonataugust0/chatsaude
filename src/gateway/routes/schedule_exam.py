from gateway.schemas.user_message_base import UserMessageBase
from services.chatbot.bot.flows.schedule_exam_flow import ScheduleExamFlow
from services.user.models.repository.user_repository import UserRepository
from .bot import Bot
from services.chatbot.bot.validators.input_validator import Input_validator
from fastapi import APIRouter, Body, Depends, HTTPException, Response, status
import re

class ScheduleExam:
    def __init__(self, tags: str = ["ScheduleExam"]):
        self.router = APIRouter(tags=tags)
        self.router.add_api_route(
            name="Registra o usuário",
            path="/insert_schedule_exam",
            endpoint=self.insert_schedule_exam,
            methods=["POST"],
            include_in_schema=True,
        )
        self.router.add_api_route(
            name="Define o nome do usuário",
            path="/set_specialty_exam",
            endpoint=self.set_specialty_exam,
            methods=["POST"],
            include_in_schema=True,
        )
        self.router.add_api_route(
            name="Define o email do usuário",
            path="/set_unity_exam",
            endpoint=self.set_unity_exam,
            methods=["POST"],
            include_in_schema=True,
        )
        self.router.add_api_route(
            name="Define o email do usuário",
            path="/set_exam_date",
            endpoint=self.set_exam_date,
            methods=["POST"],
            include_in_schema=True,
        )
        self.router.add_api_route(
            name="Define o email do usuário",
            path="/set_exam_time",
            endpoint=self.set_exam_time,
            methods=["POST"],
            include_in_schema=True,
        )
        self.router.add_api_route(
            name="Define o email do usuário",
            path="/set_necessity_exam",
            endpoint=self.set_necessity_exam,
            methods=["POST"],
            include_in_schema=True,
        )
        self.router.add_api_route(
            name="Define o email do usuário",
            path="/get_unities_exam",
            endpoint=self.get_unities_exam,
            methods=["GET"],
            include_in_schema=True,
        )

    async def insert_schedule_exam(self, params: UserMessageBase):
        message = params.results.message.value
        number = int(params.contact.urn)
        schedule_exam_entity = ScheduleExamFlow(number)
        await schedule_exam_entity.initialize()
        await schedule_exam_entity.init_exam_flow()
        return {'status': 200, 'content': 'Agendamento iniciado com sucesso'}


    async def set_specialty_exam(self, params: UserMessageBase) -> dict:
        message = params.results.message.value
        number = int(params.contact.urn)
        schedule_exam_entity = ScheduleExamFlow(number)
        await schedule_exam_entity.initialize()
        response = await schedule_exam_entity.define_specialty_exam(message)
        if 'id_especialidade' in response and response['id_especialidade'] is not None:
            return {'status': 200, 'content': 'Especialidade definida com sucesso'}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Desculpe, não foi possível identificar a especialidade solicitada, por favor, tente novamente ou entre em contato com o time de desenvolvimento através de chatsaude.al@gmail.com"
            )

    async def set_unity_exam(self, params: UserMessageBase) -> dict:
        message = params.results.message.value
        number = int(params.contact.urn)
        schedule_exam_entity = ScheduleExamFlow(number)
        await schedule_exam_entity.initialize()
        await schedule_exam_entity.define_unity_exam(message)
        last_schedule = await schedule_exam_entity.get_last_time_schedule()
        return {'status': 200, 'content': 'Unidade definida com sucesso', 'unities': last_schedule}

    async def set_exam_date(self, params: UserMessageBase) -> dict:
        message = params.results.message.value
        number = int(params.contact.urn)
        schedule_exam_entity = ScheduleExamFlow(number)
        await schedule_exam_entity.initialize()
        await schedule_exam_entity.define_date_exam(message)
        return {'status': 200, 'content': 'Data do exame definida com sucesso'}

    async def set_exam_time(self, params: UserMessageBase) -> dict:
        message = params.results.message.value
        hour = str(message).split('.')[0]
        hour = str(message).split(':')
        hour = f"{hour[0]}:{hour[1]}"
        number = int(params.contact.urn)
        schedule_exam_entity = ScheduleExamFlow(number)
        await schedule_exam_entity.initialize()
        validated_date = await schedule_exam_entity.check_conflict(hour)
        if validated_date['value']:
            await schedule_exam_entity.define_time_exam(validated_date['content'])
            return {'status': 200, 'content': 'Hora do exame definida com sucesso'}
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Desculpe, esse horário não está disponível, por favor, informe um horário posterior ao informado anteriormente para essa especialidade."
            )

    async def set_necessity_exam(self, params: UserMessageBase) -> dict:
        message = params.results.message.value
        number = int(params.contact.urn)
        schedule_exam_entity = ScheduleExamFlow(number)
        await schedule_exam_entity.initialize()
        await schedule_exam_entity.define_necessity_exam(message)
        schedule = await schedule_exam_entity.finalize_schedule_flow()
        return {'status': 200, 'content': 'Necessidade definida com sucesso', 'message': schedule}

    async def get_unities_exam(self, params: UserMessageBase) -> dict:
        message = params.results.message.value
        number = int(params.contact.urn)
        schedule_exam_entity = ScheduleExamFlow(number)
        await schedule_exam_entity.initialize()
        unities = await schedule_exam_entity.load_unities()

        padrao = r'Unidade \d+:'
        resultados = re.findall(padrao, unities)
        options = {i + 1: f'Unidade {num}' for i, num in enumerate(resultados)}
        return {'status': 200, 'content': unities, 'options': options}
