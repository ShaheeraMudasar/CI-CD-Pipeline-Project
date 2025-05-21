import asyncio

from app.routers.api import health


def test_check_health():
    response = asyncio.run(health())
    assert response.status_code == 200
    assert response.body == b'{"status":"ok"}'
