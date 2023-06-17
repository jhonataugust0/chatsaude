import os

import aiohttp
from fastapi import HTTPException, Response, status

from api.log.logging import Logging


async def send_message(message: str, number: str) -> Response | HTTPException:
    """
    Método assíncrono responsável por enviar mensagens no whatsapp
      :param message: string
      :param number: string
      return -> Response: Response object
    """
    try:
        account_sid = os.environ.get("ACCOUNT_SID")
        auth_token = os.environ.get("AUTH_TOKEN")
        from_number = os.environ.get("NUM_CHATBOT")

        async with aiohttp.ClientSession() as session:
            url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json"
            payload = {"From": from_number, "To": number, "Body": message}

            auth = aiohttp.BasicAuth(account_sid, auth_token)
            async with session.post(url, data=payload, auth=auth) as resp:
                if resp.status == 201:
                    return Response(
                        status_code=status.HTTP_200_OK,
                        content="Mensagem enviada com sucesso",
                    )
                else:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Erro ao enviar mensagem para o whatsapp",
                    )

    except Exception as error:
        message_log = "Erro ao enviar mensagem para o whatsapp"
        log = Logging(message_log)
        await log.warning(
            "#await send_message",
            None,
            str(error),
            500,
            {"params": {"message": message, "number": number}},
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message_log
        )

    finally:
        await session.close()
