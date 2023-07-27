import os
import sys
from typing import Generator

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

# adiciona o caminho do diretório raiz do projeto ao sys.path
sys.path.insert(0, PROJECT_ROOT)

# adiciona o caminho do diretório do serviço de chatbot ao sys.path
chatbot_dir = os.path.join(PROJECT_ROOT, 'api', 'services', 'chatbot')
sys.path.insert(0, chatbot_dir)

from main import app


def pytest_load_initial_conftests(early_config, parser, args):
    load_dotenv()


@pytest.fixture(scope="class")
def client() -> Generator:
    with TestClient(app) as c:
        load_dotenv()
        yield c
