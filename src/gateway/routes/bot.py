import json
from urllib.parse import parse_qs

from fastapi import (APIRouter, Body, Depends, HTTPException, Request,
                     Response, status)


from log.logging import Logging

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

    async def message(self, request: Request) -> dict:
        """
        Método responsável por escutar e tratar as mensagens
        recebidas pelo whatsapp
            :param request: Request
        """
        try:
            body = (await request.body()).decode('utf-8')
            body = json.loads(body)
            number = str(body['contact']['urn']).split('+')[1]
            number_formated = "whatsapp:+" + str(body['contact']['urn']).split('+')[1]
            message = str(body['results']['message']['value'])
            return {'status': 200, 'content': {'number': int(number), 'number_formated': number_formated, 'message': message}}

        except Exception as error:
            message_log = "Erro ao obter os dados da mensagem recebida"
            log = Logging(message_log)
            await log.warning("message", None, str(error), 500, {"params": body})
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message_log
            )
