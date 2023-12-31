from typing import Union
from fastapi import HTTPException, Response, status
from src.services.chatbot.bot.validators.document_validator import Document_validator

from src.services.chatbot.bot.validators.input_validator import Input_validator

from src.log.logging import Logging
from src.services.user.models.repository.user_repository import UserRepository
from src.services.user_flow.models.repository.fluxo_etapa_repository import FluxoEtapaRepository


class RegisterUserFlow:
    def __init__(self, number: int, lang="br") -> None:
        self.lang = lang
        self.number = number

    async def initialize(self):
        self.user = await UserRepository().select_user_from_cellphone(self.number)
        if self.user.get('id') != None:
            self.user_flow = await FluxoEtapaRepository().select_stage_from_user_id(self.user['id'])

    async def insert_user_and_flow(self, number: int) -> bool:
        user_entity = UserRepository()
        stage_entity = FluxoEtapaRepository()

        new_user = await user_entity.insert_new_user(number)
        await stage_entity.insert_new_user_flow(new_user["id"], 1, 1)
        return True

    async def define_user_name(self, message: str) -> Union[str, HTTPException]:
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
            return True

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

    async def define_user_email(self, message) -> Union[str, HTTPException]:
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
            return True

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

    async def define_user_nascent_date(self, nescient_date: str) -> Union[str, HTTPException]:
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
            return True

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

    async def define_user_cep(self, message: str) -> Union[str, HTTPException]:
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
            return True

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

    async def define_user_cpf(self, message: str) -> Union[str, HTTPException]:
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
            return True

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

    async def define_user_rg(self, message: str) -> Union[str, HTTPException]:
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
            return True

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

    async def define_user_cns(self, message: str) -> Union[str, HTTPException]:
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
            return True

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

    async def define_user_district(self, message: str) -> Union[str, HTTPException]:
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
            return True

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
