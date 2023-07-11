from api.schemas.user_message_base import UserMessageBase
from api.services.user.models.repository.user_repository import UserRepository
from .bot import Bot
from ..services.chatbot.bot.flows.register_user_flow import RegisterUserFlow
from api.services.chatbot.bot.validators.input_validator import Input_validator
from fastapi import APIRouter, Body, Depends, HTTPException, Response, status


class RegisterUser:
    def __init__(self, tags: str = ["RegisterUser"]):
        self.router = APIRouter(tags=tags)
        self.router.add_api_route(
            name="Registra o usuário",
            path="/register_user",
            endpoint=self.register_user,
            methods=["POST"],
            include_in_schema=True,
        )
        self.router.add_api_route(
            name="Define o nome do usuário",
            path="/set_name",
            endpoint=self.set_name,
            methods=["POST"],
            include_in_schema=True,
        )
        self.router.add_api_route(
            name="Define o email do usuário",
            path="/set_email",
            endpoint=self.set_email,
            methods=["POST"],
            include_in_schema=True,
        )
        self.router.add_api_route(
            name="Define o email do usuário",
            path="/set_nascient_date",
            endpoint=self.set_nascient_date,
            methods=["POST"],
            include_in_schema=True,
        )
        self.router.add_api_route(
            name="Define o email do usuário",
            path="/set_cep",
            endpoint=self.set_cep,
            methods=["POST"],
            include_in_schema=True,
        )
        self.router.add_api_route(
            name="Define o email do usuário",
            path="/set_cpf",
            endpoint=self.set_cpf,
            methods=["POST"],
            include_in_schema=True,
        )
        self.router.add_api_route(
            name="Define o email do usuário",
            path="/set_rg",
            endpoint=self.set_rg,
            methods=["POST"],
            include_in_schema=True,
        )
        self.router.add_api_route(
            name="Define o email do usuário",
            path="/set_cns",
            endpoint=self.set_cns,
            methods=["POST"],
            include_in_schema=True,
        )
        self.router.add_api_route(
            name="Define o email do usuário",
            path="/set_district",
            endpoint=self.set_district,
            methods=["POST"],
            include_in_schema=True,
        )
        self.router.add_api_route(
            name="Define o email do usuário",
            path="/verify_user_is_registered",
            endpoint=self.verify_user_is_registered,
            methods=["POST"],
            include_in_schema=True,
        )

    async def verify_user_is_registered(self, params: UserMessageBase):
        message = params.results.message.value
        number = int(params.contact.urn)
        user_entity = UserRepository()
        results = await user_entity.select_user_from_cellphone(number)
        if results.get('id') != None:
            return {'status': 200, 'content': 'Usuário registrado com sucesso'}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não registrado"
            )

    async def register_user(self, params: UserMessageBase):
        message = params.results.message.value
        number = int(params.contact.urn)
        register_user_entity = RegisterUserFlow(number)
        await register_user_entity.initialize()
        await register_user_entity.insert_user_and_flow(number)
        return {'status': 200, 'content': 'Usuário registrado com sucesso'}


    async def set_name(self, params: UserMessageBase) -> dict:
        message = params.results.message.value
        number = int(params.contact.urn)
        register_user_entity = RegisterUserFlow(number)
        await register_user_entity.initialize()
        await register_user_entity.define_user_name(message)
        return {'status': 200, 'content': 'Nome definido com sucesso'}

    async def set_email(self, params: UserMessageBase) -> dict:
        message = params.results.message.value
        number = int(params.contact.urn)
        register_user_entity = RegisterUserFlow(number)
        await register_user_entity.initialize()
        await register_user_entity.define_user_email(message)
        return {'status': 200, 'content': 'Email definido com sucesso'}

    async def set_nascient_date(self, params: UserMessageBase) -> dict:
        message = params.results.message.value
        number = int(params.contact.urn)
        register_user_entity = RegisterUserFlow(number)
        await register_user_entity.initialize()
        await register_user_entity.define_user_nascent_date(message)
        return {'status': 200, 'content': 'Data de nascimento definida com sucesso'}


    async def set_cep(self, params: UserMessageBase) -> dict:
        message = params.results.message.value
        number = int(params.contact.urn)
        register_user_entity = RegisterUserFlow(number)
        await register_user_entity.initialize()
        await register_user_entity.define_user_cep(message)
        return {'status': 200, 'content': 'CEP definido com sucesso'}

    async def set_cpf(self, params: UserMessageBase) -> dict:
        message = params.results.message.value
        number = int(params.contact.urn)
        register_user_entity = RegisterUserFlow(number)
        await register_user_entity.initialize()
        await register_user_entity.define_user_cpf(message)
        return {'status': 200, 'content': 'CPF definido com sucesso'}

    async def set_rg(self, params: UserMessageBase) -> dict:
        message = params.results.message.value
        number = int(params.contact.urn)
        register_user_entity = RegisterUserFlow(number)
        await register_user_entity.initialize()
        await register_user_entity.define_user_rg(message)
        return {'status': 200, 'content': 'RG definido com sucesso'}

    async def set_cns(self, params: UserMessageBase) -> dict:
        message = params.results.message.value
        number = int(params.contact.urn)
        register_user_entity = RegisterUserFlow(number)
        await register_user_entity.initialize()
        await register_user_entity.define_user_cns(message)
        return {'status': 200, 'content': 'CNS definida com sucesso'}

    async def set_district(self, params: UserMessageBase) -> dict:
        message = params.results.message.value
        number = int(params.contact.urn)
        register_user_entity = RegisterUserFlow(number)
        await register_user_entity.initialize()
        await register_user_entity.define_user_district(message)
        return {'status': 200, 'content': 'Data de nascimento definida com sucesso'}
