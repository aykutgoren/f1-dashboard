import pytest
import logging
from unittest.mock import AsyncMock, MagicMock
from app.services.table_creator import create_tables


class MockAsyncContextManager:
    def __init__(self, conn):
        self.conn = conn

    async def __aenter__(self):
        return self.conn

    async def __aexit__(self, exc_type, exc, tb):
        pass


@pytest.mark.asyncio
@pytest.mark.unit
async def test_create_tables_logs_success(caplog):
    # Arrange
    mock_conn = AsyncMock()
    mock_engine = MagicMock()
    mock_engine.begin.return_value = MockAsyncContextManager(mock_conn)

    caplog.set_level(logging.INFO)

    # Act
    await create_tables(mock_engine)

    # Assert
    mock_conn.run_sync.assert_called_once()
    assert "Tables created (or verified as existing)." in caplog.text


@pytest.mark.asyncio
@pytest.mark.unit
async def test_create_tables_logs_error(caplog):
    # Arrange
    mock_conn = AsyncMock()
    mock_conn.run_sync.side_effect = Exception("Test DB error")

    mock_engine = MagicMock()
    mock_engine.begin.return_value = MockAsyncContextManager(mock_conn)

    caplog.set_level(logging.ERROR)

    # Act
    await create_tables(mock_engine)

    # Assert
    assert "Error creating tables: Test DB error" in caplog.text
