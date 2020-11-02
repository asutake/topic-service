import pytest
from app.application import app


@pytest.fixture(scope='function')
def client():
    yield app.test_client()
