import datetime
import pytz
from log.logging import Logging


def validate_date(date: str):
  try:
    # Faz o split e transforma em números
    day, month, year = map(int, date.split('/'))

    if month < 1 or month > 12 or year <= 0:
      return False

    # verifica qual o último day do mês
    if month in (1, 3, 5, 7, 8, 10, 12):
      last_day = 31
    elif month == 2:
      if (year % 4 == 0) and (year % 100 != 0 or year % 400 == 0):
        last_day = 29
      else:
        last_day = 28
    else:
      last_day = 30

    
    if day < 1 or day > last_day:
      return False
    
    else:
      new_date = f"{year}-{month}-{day}"
      
      # current_hour = datetime.datetime.now(pytz.timezone("America/Sao_Paulo"))
      # current_hour = datetime.datetime.strftime(current_hour, "%Y-%m-%d %H:%M:%S")
      # current_hour = current_hour.split(' ')[0]
      
      # compare_hour = datetime.datetime.strptime(current_hour, "%Y-%m-%d")

      hour_informed = datetime.datetime.strptime(new_date,"%Y-%m-%d")
      hour_informed = datetime.datetime.strftime(hour_informed,"%Y-%m-%d")
      # if hour_informed >= compare_hour:
      #   hour_informed = datetime.datetime.strftime(hour_informed, "%Y-%m-%d")
      return {'date': hour_informed, 'value': True}

  except Exception as error:
    message_log = f'Erro ao validar a data {date}'
    log = Logging(message_log)
    log.warning('validate_email', None, str(error), 500, {'params': {'date': date}})
    # print(error)

