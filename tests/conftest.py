# tests/conftest.py
import os
import pytest

@pytest.fixture(scope="session", autouse=True)
def ensure_logs_dir():
    os.makedirs("tests/logs", exist_ok=True)
