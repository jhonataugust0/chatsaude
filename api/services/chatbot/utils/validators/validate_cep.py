import re
from fastapi import HTTPException, status
from api.log.logging import Logging

async def validate_cep(cep: str) -> bool:
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
