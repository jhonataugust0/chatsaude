from api.schemas.user_message_base import UserMessageBase
from api.services.schedules.consult.models.repository.consulta_agendameno_repository import AgendamentoConsultaRepository
from ..services.chatbot.bot.flows.schedule_consult_flow import ScheduleConsultFlow
from api.services.user.models.repository.user_repository import UserRepository
from .bot import Bot
from api.services.chatbot.bot.validators.input_validator import Input_validator
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
            endpoint=self.set_specialty,
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


    async def set_specialty(self, params: UserMessageBase) -> dict:
        message = params.results.message.value
        number = int(params.contact.urn)
        schedule_consult_entity = ScheduleConsultFlow(number)
        await schedule_consult_entity.initialize()
        await schedule_consult_entity.define_specialty_consult(message)
        return {'status': 200, 'content': 'Especialidade definida com sucesso'}

    async def set_unity_consult(self, params: UserMessageBase) -> dict:
        message = params.results.message.value
        number = int(params.contact.urn)
        schedule_consult_entity = ScheduleConsultFlow(number)
        await schedule_consult_entity.initialize()
        await schedule_consult_entity.define_unity_consult(message)
        last_schedule = await schedule_consult_entity.get_last_time_schedule()
        return {'status': 200, 'content': 'Email definido com sucesso', 'content': last_schedule}

    async def set_consult_date(self, params: UserMessageBase) -> dict:
        message = params.results.message.value
        number = int(params.contact.urn)
        validated_date = await Input_validator().validate_date_schedule(message)
        if validated_date['value']:
            schedule_consult_entity = ScheduleConsultFlow(number)
            await schedule_consult_entity.initialize()
            await schedule_consult_entity.define_date_consult(validated_date['content'])
            return {'status': 200, 'content': 'Data da consulta definida com sucesso'}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Por favor, informe uma data válida"
            )

    async def set_consult_time(self, params: UserMessageBase) -> dict:
        message = params.results.message.value
        number = int(params.contact.urn)
        validated_date = await Input_validator().check_conflict(message, number)
        if not validated_date['value']:
            schedule_consult_entity = ScheduleConsultFlow(number)
            await schedule_consult_entity.initialize()
            await schedule_consult_entity.define_time_consult(validated_date['content'])
            return {'status': 200, 'content': 'Hora da consulta definida com sucesso'}
        else:
            raise HTTPException(
                status_code=status.HTTP_401_BAD_REQUEST, detail="Não temos esse horário disponível, desculpe, por favor, informe outro"
            )

    async def set_necessity(self, params: UserMessageBase) -> dict:
        message = params.results.message.value
        number = int(params.contact.urn)
        schedule_consult_entity = ScheduleConsultFlow(number)
        await schedule_consult_entity.initialize()
        await schedule_consult_entity.define_necessity_consult(message)
        schedule = await schedule_consult_entity.finalize_schedule_flow()
        return {'status': 200, 'content': 'Necessidade definida com sucesso', 'content': schedule}

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
