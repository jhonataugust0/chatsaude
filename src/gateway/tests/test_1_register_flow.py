import datetime
import json
import httpx

from fastapi.testclient import TestClient
import pytest


# class TestRegisterFlow:
#     headers = {
#         'Accept': 'application/json',
#         "Content-Type": "application/json",
#         }
#     host = "http://localhost:8000"

#     async def request_register_user(self, payload):
#         async with httpx.AsyncClient() as client:
#             response = await client.post(self.host, headers=self.headers, json=payload)
#             response.raise_for_status()
#             return response.json()

#     @pytest.mark.asyncio
#     async def test_register_user(self):
#         payload = {
#             "contact": {
#                 "name": "",
#                 "urn": "tel:+12065551212",
#                 "uuid": "a998eda6-caaa-47d1-9ffc-3fd7a9753c84"
#             },
#             "flow": {
#                 "name": "fluxo_registro",
#                 "uuid": "5b767bce-e0e8-4211-919f-4dd6e3c46913"
#             },
#             "results": {
#                 "message": {
#                     "category": "message",
#                     "value": "1"
#                 }
#             }
#         }

#         # Crie uma instância da classe e chame o método que realiza a chamada à API
#         flow_tester = TestRegisterFlow()
#         response = await flow_tester.request_register_user(payload)

#         # Verifique se a resposta contém o status code esperado e o conteúdo esperado
#         assert response.get('status') == 200
#         assert response.get('content') == 'Usuário registrado com sucesso'
