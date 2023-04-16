from typing import Generator
import pytest
import os
import sys
from dotenv import load_dotenv
from fastapi.testclient import TestClient
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from main import app


def pytest_load_initial_conftests(early_config, parser, args):
    load_dotenv()


@pytest.fixture(scope="class")
def client() -> Generator:
    with TestClient(app) as c:
      load_dotenv()
      yield c