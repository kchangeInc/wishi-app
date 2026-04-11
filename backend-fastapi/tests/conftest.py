import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from fastapi.testclient import TestClient
from gateway.app.main import app

@pytest.fixture
def client():
    return TestClient(app)