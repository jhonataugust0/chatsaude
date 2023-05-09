import re
from fastapi import HTTPException, status
from api.log.logging import Logging


class Document_validator():

    @classmethod
    async def validate_cep(cls, cep: str) -> bool:
        """
            Verificação matemática para a validação do número do
            cartão CEP do usuário

            :params numbers: str
            return -> boolean
        """
        try:
            model = re.compile(r'^\d{5}-?\d{3}$')

            if model.match(str(cep)):
                return True
            else:
                return False
        except Exception as error:
            message_log = f"Erro ao validar o CEP {cep}"
            log = Logging(message_log)
            await log.warning(
                "validate_cpf", None, str(error), 500, {"params": {"cep": cep}}
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message_log
            )
    @classmethod
    async def validate_cns(cls, numbers: str) -> bool:
        """
        Verificação matemática para a validação do número do
        cartão do SUS do usuário

        :params numbers: str
        return -> boolean
        """
        try:
            if numbers.isdigit():
                if re.match(r"[1-2]\d{10}00[0-1]\d$", numbers) or re.match(
                    r"[7-9]\d{14}$", numbers
                ):
                    i = 0
                    soma = 0
                    while i < len(numbers):
                        soma = soma + int(numbers[i]) * (15 - i)
                        i = i + 1
                    return True if soma % 11 == 0 else False

        except Exception as error:
            message_log = f"Erro ao validar o cartão do sus {numbers}"
            log = Logging(message_log)
            await log.warning(
                "validate_cns", None, str(error), 500, {"params": {"numbers": numbers}}
            )

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message_log
            )

    @classmethod
    async def validate_cpf(cls, numbers: str) -> bool:
        """
        Verificação matemática para a validação do número de
        CPF do usuário

            :params numbers: str
            return boolean
        """
        try:
            #  Obtém os números do CPF e ignora outros caracteres
            cpf = [int(char) for char in numbers if char.isdigit()]

            #  Verifica se o CPF tem 11 dígitos
            if len(cpf) != 11:
                return False

            #  Verifica se o CPF tem todos os números iguais, ex: 111.111.111-11
            #  Esses CPFs são considerados inválidos mas passam na validação dos dígitos
            #  Antigo código para referência: if all(cpf[i] == cpf[i+1] for i in range (0, len(cpf)-1))
            if cpf == cpf[::-1]:
                return False

            #  Valida os dois dígitos verificadores
            for i in range(9, 11):
                value = sum((cpf[num] * ((i + 1) - num) for num in range(0, i)))
                digit = ((value * 10) % 11) % 10
                if digit != cpf[i]:
                    return False
            return True

        except Exception as error:
            message_log = f"Erro ao validar o CPF {numbers}"
            log = Logging(message_log)
            await log.warning(
                "validate_cpf", None, str(error), 500, {"params": {"numbers": numbers}}
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message_log
            )
