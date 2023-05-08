from urllib.parse import parse_qs

from fastapi import (APIRouter, Body, Depends, HTTPException, Request,
                     Response, status)

from api.bot.dispatcher import BotDispatcher, BotOptions
from api.bot.replies import Replies
from api.log.logging import Logging
from api.services.user_flow.models.repository.fluxo_etapa_repository import FluxoEtapaRepository
from api.services.user.models.repository.user_repository import UserRepository
from api.utils.bot_utils import send_message


class Bot:
    def __init__(self, tags: str = ["Bot"]):
        self.router = APIRouter(tags=tags)
        self.router.add_api_route(
            name="Observa o bot para responder as mensagens",
            path="/message",
            endpoint=self.message,
            methods=["POST"],
            include_in_schema=True,
        )

    async def message(self, request: Request) -> Response:
        """
        Método responsável por escutar e tratar as mensagens
        recebidas pelo whatsapp
            :param request: Request
        """
        try:
            body = (await request.body()).decode()
            body = parse_qs(body)
            message = body["Body"][0]
            number = body["WaId"][0]
            number_formated = "whatsapp:+" + str(number)

        except Exception as error:
            message_log = "Erro ao obter os dados da mensagem recebida"
            log = Logging(message_log)
            await log.warning("message", None, str(error), 500, {"params": body})
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message_log
            )

        try:
            user_entity = UserRepository()
            dispatcher = BotDispatcher()
            user = ""
            bot_response = ""

            user = await user_entity.select_user_from_cellphone(int(number))
            bot_response = await dispatcher.message_processor(message, int(number), user)
            await dispatcher.trigger_processing(bot_response, int(number), user)

        except Exception as error:
            message_log = "Erro ao tratar a mensagem recebida"
            log = Logging(message_log)
            await log.warning("message", None, str(error), 500, {"params": body})
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message
            )

        try:
            if "telefone" in user:
                stage_entity = FluxoEtapaRepository()
                user_stage = await stage_entity.select_stage_from_user_id(int(user["id"]))

                if user_stage and int(user_stage["fluxo_registro"]) == 1:
                    await dispatcher.data_users_update_flow(user, message)
                    return {}

                elif user_stage and "fluxo_agendamento_consulta" in user_stage:
                    if user_stage["fluxo_agendamento_consulta"] != "None":
                        if int(user_stage["fluxo_agendamento_consulta"]) == 1:
                            await dispatcher.data_schedule_consult_update_flow(
                                user, message
                            )

            if "message" in bot_response:
                if "telefone" in user and user["telefone"] != "None":
                    if (
                        user_stage["fluxo_agendamento_consulta"] != "None"
                        or user_stage["etapa_agendamento_consulta"] != "None"
                    ):
                        if (
                            int(user_stage["fluxo_agendamento_consulta"]) == 1
                            or int(user_stage["etapa_agendamento_consulta"]) == 1
                        ):
                            if (
                                bot_response["message"] != BotOptions.LIST_UNITIES
                                and bot_response["message"] != BotOptions.MAKE_REPORT
                                and bot_response["message"] != BotOptions.REGISTER_USER
                                and bot_response["message"] != BotOptions.SCHEDULE_CONSULT
                                and bot_response["message"] != BotOptions.SCHEDULE_EXAM
                                and bot_response["message"] != Replies.DEFAULT
                            ):
                                await send_message(bot_response["message"], number_formated)
                                return Response(
                                    status_code=status.HTTP_200_OK,
                                    content="mensagem enviada",
                                )
                        else:
                            await send_message(bot_response["message"], number_formated)
                            return Response(
                                status_code=status.HTTP_200_OK,
                                content="mensagem enviada",
                            )

                else:
                    await send_message(bot_response["message"], number_formated)
                    return Response(
                        status_code=status.HTTP_200_OK, content="mensagem enviada"
                    )

        except Exception as error:
            message_log = f"Erro ao inicializar o fluxo"
            log = Logging(message_log)
            await log.warning("message", None, str(error), 500, {"params": body})
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message
            )
