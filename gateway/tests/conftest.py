import pytest

BASE_URL = "http://127.0.0.1:8080"


@pytest.fixture
def gateway_url():
    return BASE_URL