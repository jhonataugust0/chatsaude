from dataclasses import Field
import os
from typing import Dict, List
from pydantic import BaseModel, validator, root_validator
from datetime import datetime
from datetime import date as date_type
from datetime import time as time_type

from fastapi import HTTPException
from fastapi import APIRouter, Depends, HTTPException

class Contact(BaseModel):
    name: str
    urn: str
    uuid: str

    #weni simulator
    @validator('urn', pre=True)
    def validate_urn(cls, urn):
        urn = int(str(urn.split('+')[1]))
        return int(urn)

    #whatsapp
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

    @validator('value')
    def validate_value(cls, value):
        if not isinstance(value, str):
            raise HTTPException(status_code=400, detail='O campo "value" deve ser uma string.')
        return value

class Return(BaseModel):
    category: str
    value: str

class Results(BaseModel):
    message: Message

class UserMessageBase(BaseModel):
    contact: Contact
    flow: Flow
    results: Results

    # @validator('contact', pre=True)
    # def validate_urn(cls, contact):
    #     contact['urn'] = int(str(contact['urn'].split('+')[1]))
