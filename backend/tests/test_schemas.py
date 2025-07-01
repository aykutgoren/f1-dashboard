from datetime import date

import pytest
from pydantic import ValidationError

from app.schemas.schemas import CircuitBase, DriverBase, CircuitSummary, DriverSummary


@pytest.mark.unit
def test_circuit_base_valid() -> None:
    circuit = CircuitBase(
        circuit_id=1,
        circuit_ref="monza",
        name="Autodromo Nazionale Monza",
        location="Monza",
        country="Italy",
        lat=45.6156,
        lng=9.2811,
        alt=162,
        url="http://example.com",
    )
    assert circuit.name == "Autodromo Nazionale Monza"
    assert circuit.alt == 162


@pytest.mark.unit
def test_circuit_base_optional_alt() -> None:
    circuit = CircuitBase(
        circuit_id=2,
        circuit_ref="spa",
        name="Circuit de Spa-Francorchamps",
        location="Stavelot",
        country="Belgium",
        lat=50.4372,
        lng=5.9714,
        url="http://example.com",
    )
    assert circuit.alt is None


@pytest.mark.unit
def test_driver_base_valid() -> None:
    driver = DriverBase(
        driver_id=44,
        driver_ref="hamilton",
        number=44,
        code="HAM",
        forename="Lewis",
        surname="Hamilton",
        dob=date(1985, 1, 7),
        nationality="British",
        url="http://example.com",
    )
    assert driver.forename == "Lewis"
    assert driver.number == 44


@pytest.mark.unit
def test_driver_base_missing_optional_fields() -> None:
    driver = DriverBase(
        driver_id=1,
        driver_ref="max_verstappen",
        forename="Max",
        surname="Verstappen",
        dob=date(1997, 9, 30),
        nationality="Dutch",
        url="http://example.com",
    )
    assert driver.number is None
    assert driver.code is None


@pytest.mark.unit
def test_circuit_summary_valid() -> None:
    summary = CircuitSummary(
        circuit_id=3,
        circuit_ref="silverstone",
        name="Silverstone Circuit",
        location="Silverstone",
        country="UK",
        lat=52.0786,
        lng=-1.0169,
        alt=None,
        url="http://example.com",
        fastest_lap_ms=85632,
        total_races=56,
    )
    assert summary.total_races == 56


@pytest.mark.unit
def test_driver_summary_valid() -> None:
    summary = DriverSummary(
        driver_id=33,
        driver_ref="max_verstappen",
        forename="Max",
        surname="Verstappen",
        dob=date(1997, 9, 30),
        nationality="Dutch",
        url="http://example.com",
        podiums=80,
        total_races=150,
    )
    assert summary.podiums == 80


@pytest.mark.unit
def test_driver_summary_missing_required_field() -> None:
    with pytest.raises(ValidationError) as exc_info:
        DriverSummary(
            driver_id=10,
            driver_ref="gasly",
            forename="Pierre",
            surname="Gasly",
            dob=date(1996, 2, 7),
            nationality="French",
            url="http://example.com",
            podiums=1,
            # Missing: total_races
        )
    assert "total_races" in str(exc_info.value)


@pytest.mark.unit
def test_circuit_summary_invalid_type() -> None:
    with pytest.raises(ValidationError) as exc_info:
        CircuitSummary(
            circuit_id="invalid_id",  # Should be int
            circuit_ref="test",
            name="Test Circuit",
            location="Testland",
            country="Nowhere",
            lat="not_a_float",  # Should be float
            lng=10.0,
            alt=None,
            url="http://example.com",
            fastest_lap_ms=None,
            total_races=10,
        )
    error_str = str(exc_info.value)
    assert "Input should be a valid integer" in error_str
    assert "Input should be a valid number" in error_str
