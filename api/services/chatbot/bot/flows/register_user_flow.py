from fastapi import HTTPException, Response, status
from api.services.chatbot.bot.replies import Replies
from api.services.chatbot.bot.validators.document_validator import Document_validator

from api.services.chatbot.bot.validators.input_validator import Input_validator

from .....log.logging import Logging
from ...utils.bot_utils import send_message
from api.services.user.models.repository.user_repository import UserRepository
from api.services.user_flow.models.repository.fluxo_etapa_repository import FluxoEtapaRepository


class RegisterUserFlow:
    def __init__(self, number: int, lang="br") -> None:
        self.lang = lang
        self.number = number

    async def initialize(self):
        self.user = await UserRepository().select_user_from_cellphone(self.number)
        if self.user.get('id') != None:
            self.user_flow = await FluxoEtapaRepository().select_stage_from_user_id(self.user['id'])

    # async def data_users_update_flow(self, user: dict, message: str):
    #     """
    #     Método responsável por orquestar os inputs do usuário
    #     para os métodos corretos das classes de fluxo para a
    #     execução de uma conversa com o chatbot.
    #     :params user: dict
    #     :params message: string
    #     """
    #     flow_entity = FluxoEtapaRepository()
    #     number_formated = f"whatsapp:+" + str(user["telefone"])
    #     flow_status = None

    #     try:
    #         user_flow = await flow_entity.select_stage_from_user_id(int(user["id"]))
    #         flow_status = user_flow["etapa_registro"] + 1

    #         flows = {
    #             1: RegisterUserFlow.define_user_name,
    #             2: RegisterUserFlow.define_user_email,
    #             3: RegisterUserFlow.define_user_nascent_date,
    #             4: RegisterUserFlow.define_user_cep,
    #             5: RegisterUserFlow.define_user_cpf,
    #             6: RegisterUserFlow.define_user_rg,
    #             7: RegisterUserFlow.define_user_cns,
    #             8: RegisterUserFlow.define_user_district,
    #         }

    #         validators = {
    #             2: Input_validator.validate_email,
    #             3: Input_validator.validate_nascent_date,
    #             4: Document_validator.validate_cep,
    #             5: Document_validator.validate_cpf,
    #             7: Document_validator.validate_cns,
    #         }

    #         function = flows.get(user_flow["etapa_registro"])
    #         validator = validators.get(user_flow["etapa_registro"])

    #         if validator:
    #             validated_value = await validator(message)
    #             if not validated_value['value']:
    #                 reply = "Por favor, digite um valor válido"
    #                 #await send_message(reply, number_formated)
    #                 raise HTTPException(
    #                     status_code=status.HTTP_400_BAD_REQUEST, detail=reply
    #                 )
    #             else:
    #                 # Update user data
    #                 await function(self, user, validated_value['content'], flow_status)
    #                 prompt = await Replies.get_prompt(user_flow["etapa_registro"], flow_status)
    #                 #await send_message(prompt, number_formated)

    #         elif function:
    #             await function(self, user, message, flow_status)
    #             prompt = await Replies.get_prompt(user_flow["etapa_registro"], flow_status)
    #             #await send_message(prompt, number_formated)

    #     except Exception as error:
    #         message_log = "Erro ao atualizar os dados do usuário no banco de dados"
    #         log = Logging(message_log)
    #         await log.warning(
    #             "flow_registration",
    #             None,
    #             str(error),
    #             500,
    #             {"params": {"message": message, "user": user}},
    #         )


    async def insert_user_and_flow(self, number: int):
        user_entity = UserRepository()
        stage_entity = FluxoEtapaRepository()

        new_user = await user_entity.insert_new_user(number)
        await stage_entity.insert_new_user_flow(new_user["id"], 1, 1)
        return True

    async def define_user_name(self, message: str) -> Response | HTTPException:
        """
            Método responsável por registrar o nome do usuário
            no banco de dados.
            :params user: dict
            :params message: string
            :params flow_status: int
        """
        user_entity = UserRepository()
        flow_entity = FluxoEtapaRepository()
        flow_status = self.user_flow["etapa_registro"] + 1
        try:
            await user_entity.update_user_data(
                self.user["telefone"], "nome", str(message)
            )
            await flow_entity.update_flow_from_user_id(
                self.user["id"], "etapa_registro", flow_status
            )
            return {'status': 200, 'content': "Nome definido com sucesso"}

        except Exception as error:
            message_log = "Erro ao registrar o nome do usuário no banco de dados"
            log = Logging(message_log)
            await log.warning(
                "flow_registration",
                None,
                str(error),
                500,
                {"params": {"message": message, "user": self.user, 'flow_status': self.flow_status}},
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message_log
            )

    async def define_user_email(self, message) -> Response | HTTPException:
        """
            Método responsável por registrar o email do usuário
            no banco de dados.
            :params user: dict
            :params message: string
            :params flow_status: int
        """
        user_entity = UserRepository()
        flow_entity = FluxoEtapaRepository()
        flow_status = self.user_flow["etapa_registro"] + 1
        try:
            await user_entity.update_user_data(
                self.user["telefone"], "email", str(message)
            )
            await flow_entity.update_flow_from_user_id(
                self.user["id"], "etapa_registro", flow_status
            )
            return Response(
                status_code=status.HTTP_200_OK,
                content="Email registrado com sucesso",
            )

        except Exception as error:
            message_log = "Erro ao registrar o email do usuário no banco de dados"
            log = Logging(message_log)
            await log.warning(
                "define_user_email",
                None,
                str(error),
                500,
                {"params": {"message": message, "user": self.user, 'flow_status': flow_status}},
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message_log
            )

    async def define_user_nascent_date(self, nescient_date: str) -> Response | HTTPException:
        """
            Método responsável por registrar a data de nascença
            do usuário no banco de dados.
            :params user: dict
            :params message: string
            :params flow_status: int
        """
        user_entity = UserRepository()
        flow_entity = FluxoEtapaRepository()
        flow_status = self.user_flow["etapa_registro"] + 1

        try:
            await user_entity.update_user_data(
                self.user["telefone"], "data_nascimento", nescient_date
            )
            await flow_entity.update_flow_from_user_id(
                self.user["id"], "etapa_registro", flow_status
            )
            return Response(
                status_code=status.HTTP_200_OK,
                content="Data de nascimento registrada com sucesso",
            )

        except Exception as error:
            message_log = "Erro ao registrar a data de nascimento do usuário no banco de dados"
            log = Logging(message_log)
            await log.warning(
                "define_user_nascent_date",
                None,
                str(error),
                500,
                {"params": {"nescient_date": nescient_date, "user": self.user, 'flow_status': flow_status}},
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message_log
            )

    async def define_user_cep(self, message: str) -> Response | HTTPException:
        """
            Método responsável por registrar o CEP do usuário
            no banco de dados.
            :params user: dict
            :params message: string
            :params flow_status: int
        """
        user_entity = UserRepository()
        flow_entity = FluxoEtapaRepository()
        flow_status = self.user_flow["etapa_registro"] + 1

        try:
            await user_entity.update_user_data(
                self.user["telefone"], "cep", int(message.replace("-", ""))
            )
            await flow_entity.update_flow_from_user_id(
                self.user["id"], "etapa_registro", flow_status
            )
            return Response(
                status_code=status.HTTP_200_OK,
                content="CEP registrado com sucesso",
            )

        except Exception as error:
            message_log = "Erro ao registrar o email do usuário no banco de dados"
            log = Logging(message_log)
            await log.warning(
                "define_user_cep",
                None,
                str(error),
                500,
                {"params": {"message": message, "user": self.user, 'flow_status': flow_status}},
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message_log
            )

    async def define_user_cpf(self, message: str) -> Response | HTTPException:
        """
            Método responsável por registrar o CPF do usuário
            no banco de dados.
            :params user: dict
            :params message: string
            :params flow_status: int
        """
        user_entity = UserRepository()
        flow_entity = FluxoEtapaRepository()
        flow_status = self.user_flow["etapa_registro"] + 1

        try:
            await user_entity.update_user_data(
                self.user["telefone"],
                "cpf",
                int(message),
            )
            await flow_entity.update_flow_from_user_id(
                self.user["id"], "etapa_registro", flow_status
            )
            return Response(
                status_code=status.HTTP_200_OK,
                content="CPF registrado com sucesso",
            )

        except Exception as error:
            message_log = "Erro ao registrar o CPF do usuário no banco de dados"
            log = Logging(message_log)
            await log.warning(
                "define_user_cpf",
                None,
                str(error),
                500,
                {"params": {"message": message, "user": self.user, 'flow_status': flow_status}},
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message_log
            )

    async def define_user_rg(self, message: str) -> Response | HTTPException:
        """
            Método responsável por registrar o RG do usuário
            no banco de dados.
            :params user: dict
            :params message: string
            :params flow_status: int
        """
        user_entity = UserRepository()
        flow_entity = FluxoEtapaRepository()
        flow_status = self.user_flow["etapa_registro"] + 1

        try:
            await user_entity.update_user_data(
                self.user["telefone"], "rg", int(message.replace("-", ""))
            )
            await flow_entity.update_flow_from_user_id(
                self.user["id"], "etapa_registro", flow_status
            )
            return Response(
                status_code=status.HTTP_200_OK,
                content="RG registrado com sucesso",
            )

        except Exception as error:
            message_log = "Erro ao registrar o RG do usuário no banco de dados"
            log = Logging(message_log)
            await log.warning(
                "define_user_rg",
                None,
                str(error),
                500,
                {"params": {"message": message, "user": self.user, 'flow_status': flow_status}},
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message_log
            )

    async def define_user_cns(self, message: str) -> Response | HTTPException:
        """
            Método responsável por registrar o cartão do SUS
            do usuário no banco de dados.
            :params user: dict
            :params message: string
            :params flow_status: int
        """
        user_entity = UserRepository()
        flow_entity = FluxoEtapaRepository()
        flow_status = self.user_flow["etapa_registro"] + 1

        try:
            await user_entity.update_user_data(
                self.user["telefone"],
                "c_sus",
                float(str(message).replace(".", "").replace("-", "")),
            )
            await flow_entity.update_flow_from_user_id(
                self.user["id"], "etapa_registro", flow_status
            )
            return Response(
                status_code=status.HTTP_200_OK,
                content="CNS registrado com sucesso",
            )

        except Exception as error:
            message_log = "Erro ao registrar o CNS do usuário no banco de dados"
            log = Logging(message_log)
            await log.warning(
                "define_user_cns",
                None,
                str(error),
                500,
                {"params": {"message": message, "user": self.user, 'flow_status': flow_status}},
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message_log
            )

    async def define_user_district(self, message: str) -> Response | HTTPException:
        """
            Método responsável por registrar bairro do usuário
            no banco de dados.
            :params user: dict
            :params message: string
            :params flow_status: int
        """
        user_entity = UserRepository()
        flow_entity = FluxoEtapaRepository()
        flow_status = self.user_flow["etapa_registro"] + 1

        try:
            await user_entity.update_user_data(
                self.user["telefone"], "bairro", message
            )
            await flow_entity.update_flow_from_user_id(
                self.user["id"], "fluxo_registro", 0
            )
            await flow_entity.update_flow_from_user_id(
                self.user["id"], "etapa_registro", 0
            )
            info = "Usuário cadastrado com êxito"
            log = await Logging(info).info()
            return Response(
                status_code=status.HTTP_200_OK,
                content="Bairro registrado com sucesso",
            )

        except Exception as error:
            message_log = "Erro ao registrar o bairro do usuário no banco de dados"
            log = Logging(message_log)
            await log.warning(
                "define_user_cns",
                None,
                str(error),
                500,
                {"params": {"message": message, "user": self.user, 'flow_status': flow_status}},
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message_log
            )
