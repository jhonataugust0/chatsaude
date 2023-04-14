from api.log.logging import Logging
from fastapi import HTTPException, status

def validate_cpf(numbers: str):
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
            value = sum((cpf[num] * ((i+1) - num) for num in range(0, i)))
            digit = ((value * 10) % 11) % 10
            if digit != cpf[i]:
                return False
        return True
    
    except Exception as error:
      message_log = f'Erro ao validar o CPF {numbers}'
      log = Logging(message_log)
      log.warning('validate_cpf', None, str(error), 500, {'params': {'numbers': numbers}})
      raise HTTPException(
          status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
          detail=message_log
      )