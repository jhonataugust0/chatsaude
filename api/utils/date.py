from datetime import datetime, timedelta
from fastapi import HTTPException, status
from api.log.logging import Logging


async def get_more_forty_five(init_time):
    """
      Define o horário do término do agendamento da consulta
      e/ ou do exame
        :params init_time: str
        return -> str
    """
    try:
      init_time = str(init_time) + ":00"
      convert_init_time = datetime.strptime(str(init_time), "%H:%M:%S") + timedelta(minutes=45)
      return str(convert_init_time).split(' ')[1]
    
    except Exception as error:
      message_log = 'Erro ao determinar o término da consulta'
      log = Logging(message_log)
      await log.warning('get_more_forty_five', None, str(error), 500, {'params': {'init_time': init_time}})
      raise HTTPException(
          status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
          detail=message_log
      )

async def format_date_for_user(date):
  date_formated = str(date).split('-')
  data = f"{date_formated[2]}/{date_formated[1]}/{date_formated[0]}"
  return data



async def format_time_for_user(time):
  time_formated = str(time).split(':')
  return f"{time_formated[0]}:{time_formated[1]}"

async def convert_to_datetime(time):
  return datetime.strptime(time, "%H:%M:%S")