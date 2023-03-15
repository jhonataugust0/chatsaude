from datetime import datetime, timedelta
from log.logging import Logging


def get_more_forty_five(init_time):
    """
      Define o horário do término do agendamento da consulta
      e/ ou do exame
      \n :params init_time: str
      \n return str
    """
    try:
      init_time = str(init_time) + ":00"
      convert_init_time = datetime.strptime(str(init_time), "%H:%M:%S") + timedelta(minutes=45)
      return str(convert_init_time).split(' ')[1]
    
    except Exception as error:
      message_log = 'Erro ao determinar o término da consulta'
      log = Logging(message_log)
      log.warning('get_more_forty_five', None, str(error), 500, {'params': {'init_time': init_time}})
      return False
