from fastapi.testclient import TestClient
import datetime
import json 
import requests 

class TestRegisterFlow():
  headers = {'Content-Type': 'application/x-www-form-urlencoded'}
  host = "https://f3fb-2804-29b8-5119-83a-5185-da03-e6f6-5f09.sa.ngrok.io/message"

  def test_message_default(self, client: TestClient) -> None: 
    request_body = b'SmsMessageSid=SM01cd3925943ee3504f8a5c42d88efdf6&NumMedia=0&ProfileName=Jhonata&SmsSid=SM01cd3925943ee3504f8a5c42d88efdf6&WaId=558282136275&SmsStatus=received&Body=Ol%C3%A1&To=whatsapp%3A%2B14155238886&NumSegments=1&ReferralNumMedia=0&MessageSid=SM01cd3925943ee3504f8a5c42d88efdf6&AccountSid=ACccec30b8f64bfa44a6dc60d2a447f5c5&From=whatsapp%3A%2B558282136275&ApiVersion=2010-04-01'
    request = requests.post(TestRegisterFlow.host, data=request_body, headers=TestRegisterFlow.headers)
    print(f"REQUEST\n{request}",flush=True)
    assert request.status_code == 200

  def test_init_register_flow(self, client: TestClient) -> None:
    request_body = b'SmsMessageSid=SM179ae9925ce08795ced16d3a87f66366&NumMedia=0&ProfileName=Jhonata&SmsSid=SM179ae9925ce08795ced16d3a87f66366&WaId=558282136275&SmsStatus=received&Body=1&To=whatsapp%3A%2B14155238886&NumSegments=1&ReferralNumMedia=0&MessageSid=SM179ae9925ce08795ced16d3a87f66366&AccountSid=ACccec30b8f64bfa44a6dc60d2a447f5c5&From=whatsapp%3A%2B558282136275&ApiVersion=2010-04-01'
    request = requests.post(TestRegisterFlow.host, data=request_body, headers=TestRegisterFlow.headers)
    print(f"REQUEST\n{request}",flush=True)
    assert request.status_code == 200

  def test_send_name(self, client: TestClient) -> None:
    request_body = b'SmsMessageSid=SM01cd3925943ee3504f8a5c42d88efdf6&NumMedia=0&ProfileName=Jhonata&SmsSid=SM01cd3925943ee3504f8a5c42d88efdf6&WaId=558282136275&SmsStatus=received&Body=Jhonata Augusto&To=whatsapp%3A%2B14155238886&NumSegments=1&ReferralNumMedia=0&MessageSid=SM01cd3925943ee3504f8a5c42d88efdf6&AccountSid=ACccec30b8f64bfa44a6dc60d2a447f5c5&From=whatsapp%3A%2B558282136275&ApiVersion=2010-04-01'
    request = requests.post(TestRegisterFlow.host, data=request_body, headers=TestRegisterFlow.headers)
    print(f"REQUEST\n{request}",flush=True)
    assert request.status_code == 200

  def test_send_email(self, client: TestClient) -> None:
    request_body = b'SmsMessageSid=SM01cd3925943ee3504f8a5c42d88efdf6&NumMedia=0&ProfileName=Jhonata&SmsSid=SM01cd3925943ee3504f8a5c42d88efdf6&WaId=558282136275&SmsStatus=received&Body=jhon.augustosilva@gmail.com&To=whatsapp%3A%2B14155238886&NumSegments=1&ReferralNumMedia=0&MessageSid=SM01cd3925943ee3504f8a5c42d88efdf6&AccountSid=ACccec30b8f64bfa44a6dc60d2a447f5c5&From=whatsapp%3A%2B558282136275&ApiVersion=2010-04-01'
    request = requests.post(TestRegisterFlow.host, data=request_body, headers=TestRegisterFlow.headers)
    print(f"REQUEST\n{request}",flush=True)
    assert request.status_code == 200

  def test_send_nascent_date(self, client: TestClient) -> None:
    request_body = b'SmsMessageSid=SM01cd3925943ee3504f8a5c42d88efdf6&NumMedia=0&ProfileName=Jhonata&SmsSid=SM01cd3925943ee3504f8a5c42d88efdf6&WaId=558282136275&SmsStatus=received&Body=30/10/2004&To=whatsapp%3A%2B14155238886&NumSegments=1&ReferralNumMedia=0&MessageSid=SM01cd3925943ee3504f8a5c42d88efdf6&AccountSid=ACccec30b8f64bfa44a6dc60d2a447f5c5&From=whatsapp%3A%2B558282136275&ApiVersion=2010-04-01'
    request = requests.post(TestRegisterFlow.host, data=request_body, headers=TestRegisterFlow.headers)
    print(f"REQUEST\n{request}",flush=True)
    assert request.status_code == 200

  def test_send_cep(self, client: TestClient) -> None:
    request_body = b'SmsMessageSid=SM01cd3925943ee3504f8a5c42d88efdf6&NumMedia=0&ProfileName=Jhonata&SmsSid=SM01cd3925943ee3504f8a5c42d88efdf6&WaId=558282136275&SmsStatus=received&Body=57014-630&To=whatsapp%3A%2B14155238886&NumSegments=1&ReferralNumMedia=0&MessageSid=SM01cd3925943ee3504f8a5c42d88efdf6&AccountSid=ACccec30b8f64bfa44a6dc60d2a447f5c5&From=whatsapp%3A%2B558282136275&ApiVersion=2010-04-01'
    request = requests.post(TestRegisterFlow.host, data=request_body, headers=TestRegisterFlow.headers)
    print(f"REQUEST\n{request}",flush=True)
    assert request.status_code == 200  

  def test_send_cpf(self, client: TestClient) -> None:
    request_body = b'SmsMessageSid=SM01cd3925943ee3504f8a5c42d88efdf6&NumMedia=0&ProfileName=Jhonata&SmsSid=SM01cd3925943ee3504f8a5c42d88efdf6&WaId=558282136275&SmsStatus=received&Body=112.178.614-67&To=whatsapp%3A%2B14155238886&NumSegments=1&ReferralNumMedia=0&MessageSid=SM01cd3925943ee3504f8a5c42d88efdf6&AccountSid=ACccec30b8f64bfa44a6dc60d2a447f5c5&From=whatsapp%3A%2B558282136275&ApiVersion=2010-04-01'
    request = requests.post(TestRegisterFlow.host, data=request_body, headers=TestRegisterFlow.headers)
    print(f"REQUEST\n{request}",flush=True)
    assert request.status_code == 200

  def test_send_rg(self, client: TestClient) -> None:
    request_body = b'SmsMessageSid=SM01cd3925943ee3504f8a5c42d88efdf6&NumMedia=0&ProfileName=Jhonata&SmsSid=SM01cd3925943ee3504f8a5c42d88efdf6&WaId=558282136275&SmsStatus=received&Body=4109829-3&To=whatsapp%3A%2B14155238886&NumSegments=1&ReferralNumMedia=0&MessageSid=SM01cd3925943ee3504f8a5c42d88efdf6&AccountSid=ACccec30b8f64bfa44a6dc60d2a447f5c5&From=whatsapp%3A%2B558282136275&ApiVersion=2010-04-01'
    request = requests.post(TestRegisterFlow.host, data=request_body, headers=TestRegisterFlow.headers)
    print(f"REQUEST\n{request}",flush=True)
    assert request.status_code == 200

  def test_send_sus_card(self, client: TestClient) -> None:
    request_body = b'SmsMessageSid=SM01cd3925943ee3504f8a5c42d88efdf6&NumMedia=0&ProfileName=Jhonata&SmsSid=SM01cd3925943ee3504f8a5c42d88efdf6&WaId=558282136275&SmsStatus=received&Body=145.000.875.165.186&To=whatsapp%3A%2B14155238886&NumSegments=1&ReferralNumMedia=0&MessageSid=SM01cd3925943ee3504f8a5c42d88efdf6&AccountSid=ACccec30b8f64bfa44a6dc60d2a447f5c5&From=whatsapp%3A%2B558282136275&ApiVersion=2010-04-01'
    request = requests.post(TestRegisterFlow.host, data=request_body, headers=TestRegisterFlow.headers)
    print(f"REQUEST\n{request}",flush=True)
    assert request.status_code == 200
  
  def test_send_district(self, client: TestClient) -> None:
    request_body = b'SmsMessageSid=SM01cd3925943ee3504f8a5c42d88efdf6&NumMedia=0&ProfileName=Jhonata&SmsSid=SM01cd3925943ee3504f8a5c42d88efdf6&WaId=558282136275&SmsStatus=received&Body=Vergel do lago&To=whatsapp%3A%2B14155238886&NumSegments=1&ReferralNumMedia=0&MessageSid=SM01cd3925943ee3504f8a5c42d88efdf6&AccountSid=ACccec30b8f64bfa44a6dc60d2a447f5c5&From=whatsapp%3A%2B558282136275&ApiVersion=2010-04-01'
    request = requests.post(TestRegisterFlow.host, data=request_body, headers=TestRegisterFlow.headers)
    print(f"REQUEST\n{request}",flush=True)
    assert request.status_code == 200
