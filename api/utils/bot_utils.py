import os
from fastapi import HTTPException, status, Response
from api.log.logging import Logging
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

def send_message(message: str, number: str):
  """
    Método responsável por enviar mensagens no whatsapp
      :param message: string
      :param number: string 
      return -> Response: Response object
  """
  try:
    account_sid = os.environ.get("ACCOUNT_SID")
    auth_token = os.environ.get("AUTH_TOKEN")
    client = Client(account_sid, auth_token)
    client.messages.create(from_=os.environ.get("NUM_CHATBOT"), body=message, to=number)
    return Response(
        status_code=status.HTTP_200_OK, 
        content="Mensagem enviada com sucesso"
    )
  
  except Exception as error:
    message_log = 'Erro ao enviar mensagem para o whatsapp'
    log = Logging(message_log)
    log.warning('send_message', None, str(error), 500, {'params': {'message': message, 'number': number}})
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
        detail=message_log
    )
