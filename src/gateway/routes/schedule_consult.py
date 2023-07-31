from src.gateway.schemas.user_message_base import UserMessageBase
from src.services.chatbot.bot.flows.schedule_consult_flow import ScheduleConsultFlow
from src.services.user.models.repository.user_repository import UserRepository
from .bot import Bot
from src.services.chatbot.bot.validators.input_validator import Input_validator
from fastapi import APIRouter, Body, Depends, HTTPException, Response, status
import re

class ScheduleConsult:
    def __init__(self, tags: str = ["ScheduleConsult"]):
        self.router = APIRouter(tags=tags)
        self.router.add_api_route(
            name="Registra o usuário",
            path="/insert_schedule_consult",
            endpoint=self.insert_schedule_consult,
            methods=["POST"],
            include_in_schema=True,
        )
        self.router.add_api_route(
            name="Define o nome do usuário",
            path="/set_specialty",
            endpoint=self.set_specialty_consult,
            methods=["POST"],
            include_in_schema=True,
        )
        self.router.add_api_route(
            name="Define o email do usuário",
            path="/set_unity_consult",
            endpoint=self.set_unity_consult,
            methods=["POST"],
            include_in_schema=True,
        )
        self.router.add_api_route(
            name="Define o email do usuário",
            path="/set_consult_date",
            endpoint=self.set_consult_date,
            methods=["POST"],
            include_in_schema=True,
        )
        self.router.add_api_route(
            name="Define o email do usuário",
            path="/set_consult_time",
            endpoint=self.set_consult_time,
            methods=["POST"],
            include_in_schema=True,
        )
        self.router.add_api_route(
            name="Define o email do usuário",
            path="/set_necessity",
            endpoint=self.set_necessity,
            methods=["POST"],
            include_in_schema=True,
        )
        self.router.add_api_route(
            name="Define o email do usuário",
            path="/get_unities",
            endpoint=self.get_unities,
            methods=["GET"],
            include_in_schema=True,
        )

    async def insert_schedule_consult(self, params: UserMessageBase):
        message = params.results.message.value
        number = int(params.contact.urn)
        schedule_consult_entity = ScheduleConsultFlow(number)
        await schedule_consult_entity.initialize()
        await schedule_consult_entity.init_schedule_flow()
        return {'status': 200, 'content': 'Agendamento iniciado com sucesso'}


    async def set_specialty_consult(self, params: UserMessageBase) -> dict:
        message = params.results.message.value
        number = int(params.contact.urn)
        schedule_consult_entity = ScheduleConsultFlow(number)
        await schedule_consult_entity.initialize()
        response = await schedule_consult_entity.define_specialty_consult(message)
        if 'id_especialidade' in response and response['id_especialidade'] is not None:
            return {'status': 200, 'content': 'Especialidade definida com sucesso'}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Desculpe, não foi possível identificar a especialidade solicitada, por favor, tente novamente ou entre em contato com o time de desenvolvimento através de chatsaude.al@gmail.com"
            )

    async def set_unity_consult(self, params: UserMessageBase) -> dict:
        message = params.results.message.value
        number = int(params.contact.urn)
        schedule_consult_entity = ScheduleConsultFlow(number)
        await schedule_consult_entity.initialize()
        await schedule_consult_entity.define_unity_consult(message)
        last_schedule = await schedule_consult_entity.get_last_time_schedule()
        return {'status': 200, 'content': 'Unidade definida com sucesso', 'unities': last_schedule}

    async def set_consult_date(self, params: UserMessageBase) -> dict:
        message = params.results.message.value
        number = int(params.contact.urn)
        schedule_consult_entity = ScheduleConsultFlow(number)
        await schedule_consult_entity.initialize()
        await schedule_consult_entity.define_date_consult(message)
        return {'status': 200, 'content': 'Data da consulta definida com sucesso'}

    async def set_consult_time(self, params: UserMessageBase) -> dict:
        message = params.results.message.value
        hour = message.split(':')
        hour = f"{hour[0]}:{hour[1]}"
        number = int(params.contact.urn)
        schedule_consult_entity = ScheduleConsultFlow(number)
        await schedule_consult_entity.initialize()
        validated_date = await schedule_consult_entity.check_conflict(hour)
        if validated_date['value']:
            await schedule_consult_entity.define_time_consult(validated_date['content'])
            return {'status': 200, 'content': 'Hora da consulta definida com sucesso'}
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Desculpe, esse horário não está disponível, por favor, informe um horário posterior ao informado anteriormente para essa especialidade."
            )

    async def set_necessity(self, params: UserMessageBase) -> dict:
        message = params.results.message.value
        number = int(params.contact.urn)
        schedule_consult_entity = ScheduleConsultFlow(number)
        await schedule_consult_entity.initialize()
        await schedule_consult_entity.define_necessity_consult(message)
        schedule = await schedule_consult_entity.finalize_schedule_flow()
        return {'status': 200, 'content': 'Necessidade definida com sucesso', 'message': schedule}

    async def get_unities(self, params: UserMessageBase) -> dict:
        message = params.results.message.value
        number = int(params.contact.urn)
        schedule_consult_entity = ScheduleConsultFlow(number)
        await schedule_consult_entity.initialize()
        unities = await schedule_consult_entity.load_unities()

        padrao = r'Unidade \d+:'
        resultados = re.findall(padrao, unities)
        options = {i + 1: f'Unidade {num}' for i, num in enumerate(resultados)}
        return {'status': 200, 'content': unities, 'options': options}
