import asyncio
from datetime import datetime, timedelta
import random
import httpx
from locust import HttpUser, SequentialTaskSet, task


class TestMakeSchedulingConsult(HttpUser):

    headers = {
        'Accept': 'application/json',
        "Content-Type": "application/json",
        }
    # host = "http://localhost:8000"
    host = "http://52.67.153.188"

    def generate_random_date(self):
        start_date = datetime(2023, 8, 1)
        end_date = datetime(2072, 12, 31)

        days_diff = (end_date - start_date).days

        random_days = random.randint(0, days_diff)

        random_date = start_date + timedelta(days=random_days)

        formatted_date = random_date.strftime("%Y-%m-%dT%H:%M:%S")
        return formatted_date

    def generate_random_time(self):
        start_time = datetime.strptime("00:00:00", "%H:%M:%S")
        end_time = datetime.strptime("23:59:59", "%H:%M:%S")

        time_diff = (end_time - start_time).seconds

        random_seconds = random.randint(0, time_diff)

        random_time = start_time + timedelta(seconds=random_seconds)

        formatted_time = random_time.strftime("%H:%M:%S")
        return formatted_time

    # async def client(self, route, json=payload):
    #     async with httpx.AsyncClient() as client:
    #         response =  client.post(f"{TestMakeSchedulingConsult.host}/{route}", json=payload, headers=TestMakeSchedulingConsult.headers)
    #         response.raise_for_status()
    #         return response.json()

    def test_register_user(self):
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
        response =  self.client.post("/insert_schedule_consult", json=payload)
        # assert response.get('status') == 200
        # assert response.get('content') == 'Agendamento iniciado com sucesso'


    def test_set_specialty(self):
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
        response =  self.client.post("/set_specialty", json=payload)
        # assert response.get('status') == 200
        # assert response.get('content') == 'Especialidade definida com sucesso'


    def test_set_unity(self):
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
        response =  self.client.post("/set_unity_consult", json=payload)
        # assert response.get('status') == 200
        # assert response.get('content') == 'Unidade definida com sucesso'


    def test_set_consult_date(self):
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
        response =  self.client.post("/set_consult_date", json=payload)
        # assert response.get('status') == 200
        # assert response.get('content') == 'Data da consulta definida com sucesso'


    def test_set_consult_time(self):
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
        response =  self.client.post("/set_consult_time", json=payload)
        # assert response.get('status') == 200
        # assert response.get('content') == 'Hora da consulta definida com sucesso'

    def test_set_necessity(self):
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
        response =  self.client.post("/set_necessity", json=payload)
        # assert response.get('status') == 200

    @task
    def test_scenario(self):
        self.test_register_user()
        self.test_set_specialty()
        self.test_set_unity()
        self.test_set_consult_date()
        self.test_set_consult_time()
        self.test_set_necessity()
