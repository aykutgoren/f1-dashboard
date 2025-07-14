import pytest
from sqlalchemy import text


@pytest.mark.asyncio
async def test_get_db_session_returns_valid_session(async_session):
    result = await async_session.execute(text("SELECT 1"))
    assert result.scalar_one() == 1