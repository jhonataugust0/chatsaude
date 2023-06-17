import re
import pytz
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from api.log.logging import Logging

class Input_validator():

    @classmethod
    async def validate_email(cls, email: str) -> bool:
        """
        Verifica se o email digitado pelo usuário é válido
        :params email: str
        return -> boolean
        """
        try:
            regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
            result = True if re.fullmatch(regex, email) else False
            return {'value': result, 'content': email}

        except Exception as error:
            message_log = f"Erro ao validar o email {email}"
            log = Logging(message_log)
            await log.warning(
                "validate_email", None, str(error), 500, {"params": {"email": email}}
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message_log
            )

    @classmethod
    async def validate_nascent_date(cls, date: str) -> dict[str, bool]:
        """
        Verifica a existência de uma data informada e a valida

        :params date: str
        return -> dict
        """
        try:
            # Faz o split e transforma em números
            year, month, day = map(int, date.split("-"))

            if month < 1 or month > 12 or year <= 0:
                return {'value': False, 'content': None}

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
                return {'value': False, 'content': None}

            else:
                new_date = f"{year}-{month}-{day}"

                # current_hour = datetime.datetime.now(pytz.timezone("America/Sao_Paulo"))
                # current_hour = datetime.datetime.strftime(current_hour, "%Y-%m-%d %H:%M:%S")
                # current_hour = current_hour.split(' ')[0]

                # compare_hour = datetime.datetime.strptime(current_hour, "%Y-%m-%d")

                hour_informed = datetime.strptime(new_date, "%Y-%m-%d")
                # hour_informed = datetime.datetime.strftime(hour_informed,"%Y-%m-%d")
                # if hour_informed >= compare_hour:
                #   hour_informed = datetime.datetime.strftime(hour_informed, "%Y-%m-%d")
                return {'value': True, 'content': hour_informed}

        except Exception as error:
            message_log = f"Erro ao validar a data {date}"
            log = Logging(message_log)
            await log.warning(
                "validate_email", None, str(error), 500, {"params": {"date": date}}
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message_log
            )

    async def validate_date_schedule(self, date_schedule, user=None, number_formated=None, message=None, flow_status=None):
        try:
            current_date = datetime.now(pytz.timezone("America/Sao_Paulo"))
            current_date = datetime.strftime(current_date, "%Y-%m-%d %H:%M:%S")
            current_date = current_date.split(" ")[0]

            parse_informed_date = date_schedule.split("/")
            parse_informed_date = f"{parse_informed_date[2]}-{parse_informed_date[1]}-{parse_informed_date[0]}"
            date_informed = datetime.strptime(parse_informed_date, "%Y-%m-%d")
            current_date = datetime.strptime(current_date, "%Y-%m-%d")
            # date_informed = datetime.datetime.strftime(date_informed,"%Y-%m-%d")

            if date_informed >= current_date:
                return {'value': True, 'content': date_informed}

            else:
                return {'value': False, 'content': None}

        except Exception as error:
            message_log = f"Erro ao validar a data {date_schedule}"
            log = Logging(message_log)
            await log.warning(
                "validate_email",
                None,
                str(error),
                500,
                {"params": {"date_schedule": date_schedule}},
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message_log
            )
