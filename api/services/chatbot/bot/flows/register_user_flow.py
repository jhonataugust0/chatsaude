from fastapi import HTTPException, Response, status

from .....log.logging import Logging
from ...utils.bot_utils import send_message
from api.services.user.models.repository.user_repository import UserRepository
from api.services.user_flow.models.repository.fluxo_etapa_repository import FluxoEtapaRepository


class Register_user_flow:
    def __init__(self, lang="br") -> None:
        self.lang = lang

    async def define_user_name(self, user: dict, message: str, flow_status: int) -> Response | HTTPException:
        """
            Método responsável por registrar o nome do usuário
            no banco de dados.
            :params user: dict
            :params message: string
            :params flow_status: int
        """
        user_entity = UserRepository()
        flow_entity = FluxoEtapaRepository()

        try:
            await user_entity.update_user_data(
                user["telefone"], "nome", str(message)
            )
            await flow_entity.update_flow_from_user_id(
                user["id"], "etapa_registro", flow_status
            )
            return Response(
                status_code=status.HTTP_200_OK,
                content="Nome registrado com sucesso"
            )

        except Exception as error:
            message_log = "Erro ao registrar o nome do usuário no banco de dados"
            log = Logging(message_log)
            await log.warning(
                "flow_registration",
                None,
                str(error),
                500,
                {"params": {"message": message, "user": user, 'flow_status': flow_status}},
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message_log
            )

    async def define_user_email(self, user: dict, message: str, flow_status: int) -> Response | HTTPException:
        """
            Método responsável por registrar o email do usuário
            no banco de dados.
            :params user: dict
            :params message: string
            :params flow_status: int
        """
        user_entity = UserRepository()
        flow_entity = FluxoEtapaRepository()

        try:
            await user_entity.update_user_data(
                user["telefone"], "email", str(message)
            )
            await flow_entity.update_flow_from_user_id(
                user["id"], "etapa_registro", flow_status
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
                {"params": {"message": message, "user": user, 'flow_status': flow_status}},
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message_log
            )

    async def define_user_nascent_date(self, user: dict, nescient_date: str, flow_status: int) -> Response | HTTPException:
        """
            Método responsável por registrar a data de nascença
            do usuário no banco de dados.
            :params user: dict
            :params message: string
            :params flow_status: int
        """
        user_entity = UserRepository()
        flow_entity = FluxoEtapaRepository()


        try:
            await user_entity.update_user_data(
                user["telefone"], "data_nascimento", nescient_date
            )
            await flow_entity.update_flow_from_user_id(
                user["id"], "etapa_registro", flow_status
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
                {"params": {"nescient_date": nescient_date, "user": user, 'flow_status': flow_status}},
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message_log
            )

    async def define_user_cep(self, user: dict, message: str, flow_status: int) -> Response | HTTPException:
        """
            Método responsável por registrar o CEP do usuário
            no banco de dados.
            :params user: dict
            :params message: string
            :params flow_status: int
        """
        user_entity = UserRepository()
        flow_entity = FluxoEtapaRepository()


        try:
            await user_entity.update_user_data(
                user["telefone"], "cep", int(message.replace("-", ""))
            )
            await flow_entity.update_flow_from_user_id(
                user["id"], "etapa_registro", flow_status
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
                {"params": {"message": message, "user": user, 'flow_status': flow_status}},
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message_log
            )

    async def define_user_cpf(self, user: dict, message: str, flow_status: int) -> Response | HTTPException:
        """
            Método responsável por registrar o CPF do usuário
            no banco de dados.
            :params user: dict
            :params message: string
            :params flow_status: int
        """
        user_entity = UserRepository()
        flow_entity = FluxoEtapaRepository()


        try:
            await user_entity.update_user_data(
                user["telefone"],
                "cpf",
                int(message.replace(".", "").replace("-", "")),
            )
            await flow_entity.update_flow_from_user_id(
                user["id"], "etapa_registro", flow_status
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
                {"params": {"message": message, "user": user, 'flow_status': flow_status}},
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message_log
            )

    async def define_user_rg(self, user: dict, message: str, flow_status: int) -> Response | HTTPException:
        """
            Método responsável por registrar o RG do usuário
            no banco de dados.
            :params user: dict
            :params message: string
            :params flow_status: int
        """
        user_entity = UserRepository()
        flow_entity = FluxoEtapaRepository()


        try:
            await user_entity.update_user_data(
                user["telefone"], "rg", int(message.replace("-", ""))
            )
            await flow_entity.update_flow_from_user_id(
                user["id"], "etapa_registro", flow_status
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
                {"params": {"message": message, "user": user, 'flow_status': flow_status}},
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message_log
            )

    async def define_user_cns(self, user: dict, message: str, flow_status: int) -> Response | HTTPException:
        """
            Método responsável por registrar o cartão do SUS
            do usuário no banco de dados.
            :params user: dict
            :params message: string
            :params flow_status: int
        """
        user_entity = UserRepository()
        flow_entity = FluxoEtapaRepository()


        try:
            await user_entity.update_user_data(
                user["telefone"],
                "c_sus",
                float(str(message).replace(".", "").replace("-", "")),
            )
            await flow_entity.update_flow_from_user_id(
                user["id"], "etapa_registro", flow_status
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
                {"params": {"message": message, "user": user, 'flow_status': flow_status}},
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message_log
            )

    async def define_user_district(self, user: dict, message: str, flow_status: int) -> Response | HTTPException:
        """
            Método responsável por registrar bairro do usuário
            no banco de dados.
            :params user: dict
            :params message: string
            :params flow_status: int
        """
        user_entity = UserRepository()
        flow_entity = FluxoEtapaRepository()

        try:
            await user_entity.update_user_data(
                user["telefone"], "bairro", message
            )
            await flow_entity.update_flow_from_user_id(
                user["id"], "fluxo_registro", 0
            )
            await flow_entity.update_flow_from_user_id(
                user["id"], "etapa_registro", 0
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
                {"params": {"message": message, "user": user, 'flow_status': flow_status}},
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message_log
            )
