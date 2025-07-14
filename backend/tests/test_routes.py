import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
@pytest.mark.integration
async def test_circuits_summary():
    async with AsyncClient(base_url="http://localhost:8000") as ac:
        response = await ac.get("/api/circuits/summary")
        assert response.status_code == 200


@pytest.mark.asyncio
@pytest.mark.integration
async def test_drivers_summary():
    async with AsyncClient(base_url="http://localhost:8000") as ac:
        response = await ac.get("/api/drivers/summary")
        assert response.status_code == 200
