from typing import Generator
from fastapi.testclient import TestClient
import pytest
from main import app

from dotenv import load_dotenv

def pytest_load_initial_conftests(early_config, parser, args):
    load_dotenv()

@pytest.fixture(scope="class")
def client() -> Generator:
    with TestClient(app) as c:
      load_dotenv()
      yield c