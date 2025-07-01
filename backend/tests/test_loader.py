from datetime import datetime

import pytest
import pandas as pd

from app.services.loader import _parse_date_column, _parse_time_column

@pytest.mark.unit
def test_parse_date_column():
    # Create test DataFrame
    df = pd.DataFrame(
        {"date_col": ["2021-01-01", "InvalidDate", "2022-05-06"]})

    # Expected behavior: InvalidDate should be converted to NaT (Not a Time)
    parsed_dates = _parse_date_column(df, "date_col")
    assert parsed_dates[0] == datetime(2021, 1, 1).date()
    assert pd.isna(parsed_dates[1])  # Invalid date should be NaT
    assert parsed_dates[2] == datetime(2022, 5, 6).date()

@pytest.mark.unit
def test_parse_time_column():
    # Create test DataFrame
    df = pd.DataFrame({"time_col": ["12:30:00", "InvalidTime", "15:45:30"]})

    # Expected behavior: InvalidTime should be converted to NaT (Not a Time)
    parsed_times = _parse_time_column(df, "time_col")
    assert parsed_times[0] == datetime.strptime("12:30:00", "%H:%M:%S").time()
    assert pd.isna(parsed_times[1])  # Invalid time should be NaT
    assert parsed_times[2] == datetime.strptime("15:45:30", "%H:%M:%S").time()
