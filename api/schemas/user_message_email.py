from pydantic import BaseModel, validator, root_validator
from fastapi import APIRouter, Depends, HTTPException
from datetime import time as time_type
from datetime import date as date_type
from fastapi import HTTPException
from typing import Dict, List
from datetime import datetime
import os

from api.services.chatbot.bot.validators.input_validator import Input_validator

class Contact(BaseModel):
    name: str
    urn: str
    uuid: str

class Flow(BaseModel):
    name: str
    uuid: str

class Message(BaseModel):
    category: str
    value: str

    @validator('value')
    def validate_value(cls, value):
        if not isinstance(value, str):
            raise HTTPException(status_code=400, detail='O campo "value" deve ser um texto.')
        validated_value = Input_validator().validate_email(value)
        if validated_value['value']:
            return validated_value['content']
        raise HTTPException(status_code=400, detail='Por favor, digite um email válido.')


# class Return(BaseModel):
#     category: str
#     value: str

class Results(BaseModel):
    message: Message

class UserMessageEmail(BaseModel):
    contact: Contact
    flow: Flow
    results: Results
