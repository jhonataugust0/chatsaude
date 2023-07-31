from datetime import datetime, timedelta
import json
import random
from fastapi import HTTPException
import httpx

from fastapi.testclient import TestClient
import pytest


class TestMakeSchedulingConsult:
    headers = {
        'Accept': 'application/json',
        "Content-Type": "application/json",
        }
    host = "http://localhost:8000"

    ### Utils
    def generate_random_date(self):
        start_date = datetime(2023, 8, 1)
        end_date = datetime(2072, 12, 31)

        days_diff = (end_date - start_date).days

        random_days = random.randint(0, days_diff)

        random_date = start_date + timedelta(days=random_days)

        formatted_date = random_date.strftime("%Y-%m-%dT")
        print(f"DATA {formatted_date}", flush=True)
        return formatted_date

    def generate_random_time(self):
        start_time = datetime.strptime("00:00:00", "%H:%M:%S")
        end_time = datetime.strptime("23:59:59", "%H:%M:%S")

        time_diff = (end_time - start_time).seconds

        random_seconds = random.randint(0, time_diff)

        random_time = start_time + timedelta(seconds=random_seconds)

        formatted_time = random_time.strftime("%H:%M:%S")
        print(f"DATA {formatted_time}", flush=True)
        return formatted_time



    async def request_register_consult(self, payload):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{TestMakeSchedulingConsult.host}/insert_schedule_consult",
                headers=TestMakeSchedulingConsult.headers,
                json=payload
            )
            response.raise_for_status()
            return response.json()

    async def request_specialty_consult(self, payload):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{TestMakeSchedulingConsult.host}/set_specialty",
                headers=TestMakeSchedulingConsult.headers,
                json=payload
            )
            response.raise_for_status()
            return response.json()

    async def request_unity_consult(self, payload):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{TestMakeSchedulingConsult.host}/set_unity_consult",
                headers=TestMakeSchedulingConsult.headers,
                json=payload
            )
            response.raise_for_status()
            return response.json()

    async def request_date_consult(self, payload):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{TestMakeSchedulingConsult.host}/set_consult_date",
                headers=TestMakeSchedulingConsult.headers,
                json=payload
            )
            response.raise_for_status()
            return response.json()

    async def request_time_consult(self, payload):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{TestMakeSchedulingConsult.host}/set_consult_time",
                headers=TestMakeSchedulingConsult.headers,
                json=payload
            )
            response.raise_for_status()
            return response.json()

    async def request_necessity_consult(self, payload):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{TestMakeSchedulingConsult.host}/set_necessity",
                headers=TestMakeSchedulingConsult.headers,
                json=payload
            )
            response.raise_for_status()
            return response.json()

    @pytest.mark.asyncio
    async def test_register_user(self):
        payload = {
            "contact": {
                "name": "",
                "urn": "tel:+12065551212",
                "uuid": "a998eda6-caaa-47d1-9ffc-3fd7a9753c84"
            },
            "flow": {
                "name": "fluxo_registro",
                "uuid": "5b767bce-e0e8-4211-919f-4dd6e3c46913"
            },
            "results": {
                "message": {
                    "category": "message",
                    "value": "1"
                }
            }
        }
        response = await self.request_register_consult(payload)
        assert response.get('status') == 200
        assert response.get('content') == 'Agendamento iniciado com sucesso'

    @pytest.mark.asyncio
    async def test_set_specialty(self):
        payload = {
            "contact": {
                "name": "",
                "urn": "tel:+12065551212",
                "uuid": "a998eda6-caaa-47d1-9ffc-3fd7a9753c84"
            },
            "flow": {
                "name": "fluxo_registro",
                "uuid": "5b767bce-e0e8-4211-919f-4dd6e3c46913"
            },
            "results": {
                "message": {
                    "category": "specialty",
                    "value": "Clínico"
                }
            }
        }
        response = await self.request_specialty_consult(payload)
        assert response.get('status') == 200
        assert response.get('content') == 'Especialidade definida com sucesso'

    # @pytest.mark.asyncio
    # async def test_fail_set_specialty(self):
    #     payload = {
    #         "contact": {
    #             "name": "",
    #             "urn": "tel:+12065551212",
    #             "uuid": "a998eda6-caaa-47d1-9ffc-3fd7a9753c84"
    #         },
    #         "flow": {
    #             "name": "fluxo_registro",
    #             "uuid": "5b767bce-e0e8-4211-919f-4dd6e3c46913"
    #         },
    #         "results": {
    #             "message": {
    #                 "category": "specialty",
    #                 "value": "Mecânico de retroescavadeira"
    #             }
    #         }
    #     }
    #     flow_tester = TestMakeSchedulingConsult()
    #     with pytest.raises(HTTPException) as exc_info:
    #         await flow_tester.request_specialty_consult(payload)
    #     assert exc_info.value.status_code == 404
    #     assert exc_info.value.detail == 'Desculpe, não foi possível identificar a especialidade solicitada, por favor, tente novamente ou entre em contato com o time de desenvolvimento através de chatsaude.al@gmail.com'

    @pytest.mark.asyncio
    async def test_set_unity(self):
        payload = {
            "contact": {
                "name": "",
                "urn": "tel:+12065551212",
                "uuid": "a998eda6-caaa-47d1-9ffc-3fd7a9753c84"
            },
            "flow": {
                "name": "fluxo_registro",
                "uuid": "5b767bce-e0e8-4211-919f-4dd6e3c46913"
            },
            "results": {
                "message": {
                    "category": "message",
                    "value": "1"
                }
            }
        }
        response = await self.request_unity_consult(payload)
        assert response.get('status') == 200
        assert response.get('content') == 'Unidade definida com sucesso'

    @pytest.mark.asyncio
    async def test_set_consult_date(self):
        payload = {
            "contact": {
                "name": "",
                "urn": "tel:+12065551212",
                "uuid": "a998eda6-caaa-47d1-9ffc-3fd7a9753c84"
            },
            "flow": {
                "name": "fluxo_registro",
                "uuid": "5b767bce-e0e8-4211-919f-4dd6e3c46913"
            },
            "results": {
                "message": {
                    "category": "date_schedule",
                    "value": self.generate_random_date()
                }
            }
        }
        response = await self.request_date_consult(payload)
        assert response.get('status') == 200
        assert response.get('content') == 'Data da consulta definida com sucesso'

    @pytest.mark.asyncio
    async def test_set_consult_time(self):
        payload = {
            "contact": {
                "name": "",
                "urn": "tel:+12065551212",
                "uuid": "a998eda6-caaa-47d1-9ffc-3fd7a9753c84"
            },
            "flow": {
                "name": "fluxo_registro",
                "uuid": "5b767bce-e0e8-4211-919f-4dd6e3c46913"
            },
            "results": {
                "message": {
                    "category": "time_schedule",
                    "value": self.generate_random_time()
                }
            }
        }
        response = await self.request_time_consult(payload)
        assert response.get('status') == 200
        assert response.get('content') == 'Hora da consulta definida com sucesso'

    @pytest.mark.asyncio
    async def test_set_necessity(self):
        payload = {
            "contact": {
                "name": "",
                "urn": "tel:+12065551212",
                "uuid": "a998eda6-caaa-47d1-9ffc-3fd7a9753c84"
            },
            "flow": {
                "name": "fluxo_registro",
                "uuid": "5b767bce-e0e8-4211-919f-4dd6e3c46913"
            },
            "results": {
                "message": {
                    "category": "necessity",
                    "value": "Finalizar"
                }
            }
        }
        response = await self.request_necessity_consult(payload)
        assert response.get('status') == 200
