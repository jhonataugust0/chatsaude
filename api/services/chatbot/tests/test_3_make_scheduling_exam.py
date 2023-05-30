import datetime
import json

from fastapi.testclient import TestClient


class TestRegisterFlow:
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    # host = "https://5156-2804-29b8-5119-83a-5185-da03-e6f6-5f09.sa.ngrok.io/message"
    host = "http://localhost:8000"

    def test_message_default(self, client: TestClient) -> None:
        request_body = b"SmsMessageSid=SM01cd3925943ee3504f8a5c42d88efdf6&NumMedia=0&ProfileName=Jhonata&SmsSid=SM01cd3925943ee3504f8a5c42d88efdf6&WaId=558282136275&SmsStatus=received&Body=Ol%C3%A1&To=whatsapp%3A%2B14155238886&NumSegments=1&ReferralNumMedia=0&MessageSid=SM01cd3925943ee3504f8a5c42d88efdf6&AccountSid=ACccec30b8f64bfa44a6dc60d2a447f5c5&From=whatsapp%3A%2B558282136275&ApiVersion=2010-04-01"
        request = client.post(
            "/message", data=request_body, headers=TestRegisterFlow.headers
        )
        print(f"REQUEST\n{request}", flush=True)
        assert request.status_code == 200

    def test_init_scheduling_flow(self, client: TestClient) -> None:
        request_body = b"SmsMessageSid=SM179ae9925ce08795ced16d3a87f66366&NumMedia=0&ProfileName=Jhonata&SmsSid=SM179ae9925ce08795ced16d3a87f66366&WaId=558282136275&SmsStatus=received&Body=3&To=whatsapp%3A%2B14155238886&NumSegments=1&ReferralNumMedia=0&MessageSid=SM179ae9925ce08795ced16d3a87f66366&AccountSid=ACccec30b8f64bfa44a6dc60d2a447f5c5&From=whatsapp%3A%2B558282136275&ApiVersion=2010-04-01"
        request = client.post(
            "/message", data=request_body, headers=TestRegisterFlow.headers
        )
        print(f"REQUEST\n{request}", flush=True)
        assert request.status_code == 200

    def test_send_specialty(self, client: TestClient) -> None:
        request_body = b"SmsMessageSid=SM01cd3925943ee3504f8a5c42d88efdf6&NumMedia=0&ProfileName=Jhonata&SmsSid=SM01cd3925943ee3504f8a5c42d88efdf6&WaId=558282136275&SmsStatus=received&Body=Exame de sangue&To=whatsapp%3A%2B14155238886&NumSegments=1&ReferralNumMedia=0&MessageSid=SM01cd3925943ee3504f8a5c42d88efdf6&AccountSid=ACccec30b8f64bfa44a6dc60d2a447f5c5&From=whatsapp%3A%2B558282136275&ApiVersion=2010-04-01"
        request = client.post(
            "/message", data=request_body, headers=TestRegisterFlow.headers
        )
        print(f"REQUEST\n{request}", flush=True)
        assert request.status_code == 200

    def test_send_unity(self, client: TestClient) -> None:
        request_body = b"SmsMessageSid=SM01cd3925943ee3504f8a5c42d88efdf6&NumMedia=0&ProfileName=Jhonata&SmsSid=SM01cd3925943ee3504f8a5c42d88efdf6&WaId=558282136275&SmsStatus=received&Body=1&To=whatsapp%3A%2B14155238886&NumSegments=1&ReferralNumMedia=0&MessageSid=SM01cd3925943ee3504f8a5c42d88efdf6&AccountSid=ACccec30b8f64bfa44a6dc60d2a447f5c5&From=whatsapp%3A%2B558282136275&ApiVersion=2010-04-01"
        request = client.post(
            "/message", data=request_body, headers=TestRegisterFlow.headers
        )
        print(f"REQUEST\n{request}", flush=True)
        assert request.status_code == 200

    def test_send_schedule_date(self, client: TestClient) -> None:
        request_body = b"SmsMessageSid=SM01cd3925943ee3504f8a5c42d88efdf6&NumMedia=0&ProfileName=Jhonata&SmsSid=SM01cd3925943ee3504f8a5c42d88efdf6&WaId=558282136275&SmsStatus=received&Body=13/08/2023&To=whatsapp%3A%2B14155238886&NumSegments=1&ReferralNumMedia=0&MessageSid=SM01cd3925943ee3504f8a5c42d88efdf6&AccountSid=ACccec30b8f64bfa44a6dc60d2a447f5c5&From=whatsapp%3A%2B558282136275&ApiVersion=2010-04-01"
        request = client.post(
            "/message", data=request_body, headers=TestRegisterFlow.headers
        )
        print(f"REQUEST\n{request}", flush=True)
        assert request.status_code == 200

    def test_send_init_schedule_time(self, client: TestClient) -> None:
        request_body = b"SmsMessageSid=SM01cd3925943ee3504f8a5c42d88efdf6&NumMedia=0&ProfileName=Jhonata&SmsSid=SM01cd3925943ee3504f8a5c42d88efdf6&WaId=558282136275&SmsStatus=received&Body=11:00&To=whatsapp%3A%2B14155238886&NumSegments=1&ReferralNumMedia=0&MessageSid=SM01cd3925943ee3504f8a5c42d88efdf6&AccountSid=ACccec30b8f64bfa44a6dc60d2a447f5c5&From=whatsapp%3A%2B558282136275&ApiVersion=2010-04-01"
        request = client.post(
            "/message", data=request_body, headers=TestRegisterFlow.headers
        )
        print(f"REQUEST\n{request}", flush=True)
        assert request.status_code == 200

    def test_send_necessity_description(self, client: TestClient) -> None:
        request_body = b"SmsMessageSid=SM01cd3925943ee3504f8a5c42d88efdf6&NumMedia=0&ProfileName=Jhonata&SmsSid=SM01cd3925943ee3504f8a5c42d88efdf6&WaId=558282136275&SmsStatus=received&Body=analise de creatinina&To=whatsapp%3A%2B14155238886&NumSegments=1&ReferralNumMedia=0&MessageSid=SM01cd3925943ee3504f8a5c42d88efdf6&AccountSid=ACccec30b8f64bfa44a6dc60d2a447f5c5&From=whatsapp%3A%2B558282136275&ApiVersion=2010-04-01"
        request = client.post(
            "/message", data=request_body, headers=TestRegisterFlow.headers
        )
        print(f"REQUEST\n{request}", flush=True)
        assert request.status_code == 200
