import re
from fastapi import HTTPException, status
from log.logging import Logging


class Document_validator():

    @staticmethod
    def validate_cep(cep: str)  -> dict:
        """
            Verificação matemática para a validação do número do
            cartão CEP do usuário

            :params numbers: str
            return -> boolean
        """
        try:
            model = re.compile(r'^\d{5}-?\d{3}$')

            if model.match(str(cep.replace('-','').replace(' ', ''))):
                return {'value': True, 'content': cep}
            else:
                return {'value': False, 'content': None}

        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro ao validar cep {cep}"
            )

    @staticmethod
    def validate_cns(numbers: str)  -> dict:
        """
        Verificação matemática para a validação do número do
        cartão do SUS do usuário

        :params numbers: str
        return -> boolean
        """
        try:
            number = str(numbers.replace(',', '').replace('-', '').replace('.', ''))
            if re.match(r"[1-2]\d{10}00[0-1]\d$", number) or re.match(
                r"[7-9]\d{14}$", number
            ):
                i = 0
                soma = 0
                while i < len(number):
                    soma = soma + int(number[i]) * (15 - i)
                    i = i + 1
                if soma % 11 == 0:
                    return {'value': True, 'content': number}
                else:
                    return {'value': False, 'content': None}

        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro ao validar o cartão do sus {numbers}"
            )

    @staticmethod
    def validate_cpf(numbers: str)  -> dict:
        """
        Verificação matemática para a validação do número de
        CPF do usuário

            :params numbers: str
            return boolean
        """
        try:
            #  Obtém os números do CPF e ignora outros caracteres
            numbers = numbers.replace('.', '').replace('-', '')
            cpf = [int(char) for char in numbers if char.isdigit()]

            #  Verifica se o CPF tem 11 dígitos
            if len(cpf) != 11:
                return {'value': False, 'content': None}

            #  Verifica se o CPF tem todos os números iguais, ex: 111.111.111-11
            #  Esses CPFs são considerados inválidos mas passam na validação dos dígitos
            #  Antigo código para referência: if all(cpf[i] == cpf[i+1] for i in range (0, len(cpf)-1))
            if cpf == cpf[::-1]:
                return {'value': False, 'content': None}

            #  Valida os dois dígitos verificadores
            for i in range(9, 11):
                value = sum((cpf[num] * ((i + 1) - num) for num in range(0, i)))
                digit = ((value * 10) % 11) % 10
                if digit != cpf[i]:
                    return {'value': False, 'content': None}
            result = bool(int(''.join(str(x) for x in cpf)))
            dict = {'value': result, 'content': numbers}
            return dict

        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro ao validar o CPF {numbers}"
            )
