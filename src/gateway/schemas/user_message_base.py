from pydantic import BaseModel, ValidationError, validator, root_validator, fields
from datetime import datetime

from fastapi import HTTPException
from fastapi import APIRouter, Depends, HTTPException
from services.chatbot.bot.validators.document_validator import Document_validator

from services.chatbot.bot.validators.input_validator import Input_validator


class Contact(BaseModel):
    name: str
    urn: str
    uuid: str

    # weni simulator
    @validator("urn", pre=True)
    def validate_urn(cls, urn):
        urn = int(str(urn.split("+")[1]))
        return int(urn)

    # whatsapp
    # @validator('urn', pre=True)
    # def validate_urn(cls, urn):
    #     urn = int(str(urn.split(':')[1]))
    #     return int(urn)


class Flow(BaseModel):
    name: str
    uuid: str


class Message(BaseModel):
    category: str
    value: str

    @root_validator(pre=True)
    def validate_field(cls, values):
        types_validators = {
            "message": Input_validator.validate_message,
            'email': Input_validator.validate_email,
            'date_nascient': Input_validator.validate_nascent_date,
            'cep': Document_validator.validate_cep,
            'cpf': Document_validator.validate_cpf,
            'cns': Document_validator.validate_cns,
            'date_schedule': Input_validator.validate_date_schedule,
        }

        category = values.get('category')
        if category in types_validators:
            validator_func = types_validators[category]
            result_func = validator_func(values.get('value'))
            if result_func['value']:
                values['value'] = result_func['content']
                return values
            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"O valor informado para {category} não é válido",
                )
        return values


class Return(BaseModel):
    category: str
    value: str

class Results(BaseModel):
    message: Message


class UserMessageBase(BaseModel):
    contact: Contact
    flow: Flow
    results: Results
