from ..routes.bot import Bot
from ..services.chatbot.bot.flows.register_user_flow import RegisterUserFlow
from api.services.chatbot.bot.validators.input_validator import Input_validator
from fastapi import APIRouter, Body, Depends, HTTPException, Request, Response, status


class User:
    def __init__(self, tags: str = ["User"]):
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

    async def register_user(self, request: Request):
        bot_message = Bot()
        input = await bot_message.message(request)
        message = input['content']['message']
        number = input['content']['number']
        register_user_entity = RegisterUserFlow(number)
        await register_user_entity.initialize()
        await register_user_entity.insert_user_and_flow(number)
        return {'status': 200, 'content': 'Usuário registrado com sucesso'}


    async def set_name(self, request: Request):
        bot_message = Bot()
        input = await bot_message.message(request)
        message = input['content']['message']
        number = input['content']['number']
        register_user_entity = RegisterUserFlow(number)
        await register_user_entity.initialize()
        await register_user_entity.define_user_name(message)
        return {'status': 200, 'content': 'Nome definido com sucesso'}

    async def set_email(self, request: Request):
        bot_message = Bot()
        input = await bot_message.message(request)
        message = input['content']['message']
        number = input['content']['number']
        register_user_entity = RegisterUserFlow(number)
        await register_user_entity.initialize()
        await register_user_entity.define_user_email(message)
        return {'status': 200, 'content': 'Email definido com sucesso'}

    async def set_nascient_date(self, request: Request):
        bot_message = Bot()
        input = await bot_message.message(request)
        message = input['content']['message'].split('T')[0]
        number = input['content']['number']
        validated_date = await Input_validator.validate_nascent_date(message)
        if validated_date['value']:
            register_user_entity = RegisterUserFlow(number)
            await register_user_entity.initialize()
            await register_user_entity.define_user_nascent_date(validated_date['content'])
            return {'status': 200, 'content': 'Data de nascimento definida com sucesso'}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Por favor, digite uma data válida"
            )

    async def set_cep(self, request: Request):
        bot_message = Bot()
        input = await bot_message.message(request)
        message = input['content']['message']
        number = input['content']['number']
        register_user_entity = RegisterUserFlow(number)
        await register_user_entity.initialize()
        await register_user_entity.define_user_cep(message)
        return {'status': 200, 'content': 'CEP definido com sucesso'}

    async def set_cpf(self, request: Request):
        bot_message = Bot()
        input = await bot_message.message(request)
        message = input['content']['message']
        number = input['content']['number']
        register_user_entity = RegisterUserFlow(number)
        await register_user_entity.initialize()
        await register_user_entity.define_user_cpf(message)
        return {'status': 200, 'content': 'CPF definido com sucesso'}

    async def set_rg(self, request: Request):
        bot_message = Bot()
        input = await bot_message.message(request)
        message = input['content']['message']
        number = input['content']['number']
        register_user_entity = RegisterUserFlow(number)
        await register_user_entity.initialize()
        await register_user_entity.define_user_rg(message)
        return {'status': 200, 'content': 'RG definido com sucesso'}

    async def set_cns(self, request: Request):
        bot_message = Bot()
        input = await bot_message.message(request)
        message = input['content']['message']
        number = input['content']['number']
        register_user_entity = RegisterUserFlow(number)
        await register_user_entity.initialize()
        await register_user_entity.define_user_cns(message)
        return {'status': 200, 'content': 'CNS definida com sucesso'}

    async def set_district(self, request: Request):
        bot_message = Bot()
        input = await bot_message.message(request)
        message = input['content']['message']
        number = input['content']['number']
        register_user_entity = RegisterUserFlow(number)
        await register_user_entity.initialize()
        await register_user_entity.define_user_district(message)
        return {'status': 200, 'content': 'Data de nascimento definida com sucesso'}
