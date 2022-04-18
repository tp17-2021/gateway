import nest_asyncio
nest_asyncio.apply()
__import__('IPython').embed()

import requests
from fastapi.testclient import TestClient
import pytest

with mock.patch.dict(os.environ, os.environ):
    from src.main import app


client = TestClient(app)


def test_it_should_work_base_url():
    response = client.get("/")
    assert response.status_code == 200, "Base url not working"


# @pytest.mark.asyncio
# async def test_it_should_accept_valid_vote():
