import re
from log.logging import Logging


def validate_cns(numbers: str):
    try:
      if numbers.isdigit():
        if re.match(r'[1-2]\d{10}00[0-1]\d$',numbers) or re.match(r'[7-9]\d{14}$',numbers):
            i = 0
            soma = 0
            while i<len(numbers):
                soma = soma+int(numbers[i]) * (15 - i)
                i = i+1
            return True if soma % 11 == 0 else False
    
    except Exception as error:
      message_log = f'Erro ao validar o cartão do sus {numbers}'
      log = Logging(message_log)
      log.warning('validate_cns', None, str(error), 500, {'params': {'numbers': numbers}})
