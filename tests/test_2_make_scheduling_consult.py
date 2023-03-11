from fastapi.testclient import TestClient
import datetime
import json 
import requests 

class TestRegisterFlow():
  headers = {'Content-Type': 'application/x-www-form-urlencoded'}
  host = "https://8188-187-19-172-237.sa.ngrok.io/message"

  def test_message_default(self, client: TestClient) -> None: 
    request_body = b'SmsMessageSid=SM01cd3925943ee3504f8a5c42d88efdf6&NumMedia=0&ProfileName=Jhonata&SmsSid=SM01cd3925943ee3504f8a5c42d88efdf6&WaId=558282136275&SmsStatus=received&Body=Ol%C3%A1&To=whatsapp%3A%2B14155238886&NumSegments=1&ReferralNumMedia=0&MessageSid=SM01cd3925943ee3504f8a5c42d88efdf6&AccountSid=ACccec30b8f64bfa44a6dc60d2a447f5c5&From=whatsapp%3A%2B558282136275&ApiVersion=2010-04-01'
    request = requests.post(TestRegisterFlow.host, data=request_body, headers=TestRegisterFlow.headers)
    print(f"REQUEST\n{request}",flush=True)
    assert request.status_code == 200

  def test_init_scheduling_flow(self, client: TestClient) -> None:
    request_body = b'SmsMessageSid=SM179ae9925ce08795ced16d3a87f66366&NumMedia=0&ProfileName=Jhonata&SmsSid=SM179ae9925ce08795ced16d3a87f66366&WaId=558282136275&SmsStatus=received&Body=2&To=whatsapp%3A%2B14155238886&NumSegments=1&ReferralNumMedia=0&MessageSid=SM179ae9925ce08795ced16d3a87f66366&AccountSid=ACccec30b8f64bfa44a6dc60d2a447f5c5&From=whatsapp%3A%2B558282136275&ApiVersion=2010-04-01'
    request = requests.post(TestRegisterFlow.host, data=request_body, headers=TestRegisterFlow.headers)
    print(f"REQUEST\n{request}",flush=True)
    assert request.status_code == 200

  def test_send_specialty(self, client: TestClient) -> None:
    request_body = b'SmsMessageSid=SM01cd3925943ee3504f8a5c42d88efdf6&NumMedia=0&ProfileName=Jhonata&SmsSid=SM01cd3925943ee3504f8a5c42d88efdf6&WaId=558282136275&SmsStatus=received&Body=Cl%C3%ADnico&To=whatsapp%3A%2B14155238886&NumSegments=1&ReferralNumMedia=0&MessageSid=SM01cd3925943ee3504f8a5c42d88efdf6&AccountSid=ACccec30b8f64bfa44a6dc60d2a447f5c5&From=whatsapp%3A%2B558282136275&ApiVersion=2010-04-01'
    request = requests.post(TestRegisterFlow.host, data=request_body, headers=TestRegisterFlow.headers)
    print(f"REQUEST\n{request}",flush=True)
    assert request.status_code == 200

  def test_send_unity(self, client: TestClient) -> None:
    request_body = b'SmsMessageSid=SM01cd3925943ee3504f8a5c42d88efdf6&NumMedia=0&ProfileName=Jhonata&SmsSid=SM01cd3925943ee3504f8a5c42d88efdf6&WaId=558282136275&SmsStatus=received&Body=3&To=whatsapp%3A%2B14155238886&NumSegments=1&ReferralNumMedia=0&MessageSid=SM01cd3925943ee3504f8a5c42d88efdf6&AccountSid=ACccec30b8f64bfa44a6dc60d2a447f5c5&From=whatsapp%3A%2B558282136275&ApiVersion=2010-04-01'
    request = requests.post(TestRegisterFlow.host, data=request_body, headers=TestRegisterFlow.headers)
    print(f"REQUEST\n{request}",flush=True)
    assert request.status_code == 200

  def test_send_schedule_date(self, client: TestClient) -> None:
    request_body = b'SmsMessageSid=SM01cd3925943ee3504f8a5c42d88efdf6&NumMedia=0&ProfileName=Jhonata&SmsSid=SM01cd3925943ee3504f8a5c42d88efdf6&WaId=558282136275&SmsStatus=received&Body=21/03/2023&To=whatsapp%3A%2B14155238886&NumSegments=1&ReferralNumMedia=0&MessageSid=SM01cd3925943ee3504f8a5c42d88efdf6&AccountSid=ACccec30b8f64bfa44a6dc60d2a447f5c5&From=whatsapp%3A%2B558282136275&ApiVersion=2010-04-01'
    request = requests.post(TestRegisterFlow.host, data=request_body, headers=TestRegisterFlow.headers)
    print(f"REQUEST\n{request}",flush=True)
    assert request.status_code == 200

  def test_send_init_schedule_time(self, client: TestClient) -> None:
    request_body = b'SmsMessageSid=SM01cd3925943ee3504f8a5c42d88efdf6&NumMedia=0&ProfileName=Jhonata&SmsSid=SM01cd3925943ee3504f8a5c42d88efdf6&WaId=558282136275&SmsStatus=received&Body=08:00&To=whatsapp%3A%2B14155238886&NumSegments=1&ReferralNumMedia=0&MessageSid=SM01cd3925943ee3504f8a5c42d88efdf6&AccountSid=ACccec30b8f64bfa44a6dc60d2a447f5c5&From=whatsapp%3A%2B558282136275&ApiVersion=2010-04-01'
    request = requests.post(TestRegisterFlow.host, data=request_body, headers=TestRegisterFlow.headers)
    print(f"REQUEST\n{request}",flush=True)
    assert request.status_code == 200  

  def test_send_necessity_description(self, client: TestClient) -> None:
    request_body = b'SmsMessageSid=SM01cd3925943ee3504f8a5c42d88efdf6&NumMedia=0&ProfileName=Jhonata&SmsSid=SM01cd3925943ee3504f8a5c42d88efdf6&WaId=558282136275&SmsStatus=received&Body=Dor de dente&To=whatsapp%3A%2B14155238886&NumSegments=1&ReferralNumMedia=0&MessageSid=SM01cd3925943ee3504f8a5c42d88efdf6&AccountSid=ACccec30b8f64bfa44a6dc60d2a447f5c5&From=whatsapp%3A%2B558282136275&ApiVersion=2010-04-01'
    request = requests.post(TestRegisterFlow.host, data=request_body, headers=TestRegisterFlow.headers)
    print(f"REQUEST\n{request}",flush=True)
    assert request.status_code == 200