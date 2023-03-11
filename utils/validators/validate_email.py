import re
from log.logging import Logging

def validate_email(email: str):
  """
    Verifica se o email digitado pelo usuário é válido
      :params email: str
  """
  try:
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    return True if (re.fullmatch(regex, email)) else False

  except Exception as error:
    message_log = f'Erro ao validar o email {email}'
    log = Logging(message_log)
    log.warning('validate_email', None, str(error), 500, {'params': {'email': email}})