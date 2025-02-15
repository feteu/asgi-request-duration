from typing import Type
import pytest
from asgi_request_duration.constants import _DEFAULT_HEADER_NAME, _DEFAULT_PRECISION
from asgi_request_duration.decorators import validate_header_name, validate_precision
from asgi_request_duration.exceptions import InvalidHeaderNameException, PrecisionValueOutOfRangeException

class TestClass:
    def __init__(self, header_name: str = _DEFAULT_HEADER_NAME, precision: int = _DEFAULT_PRECISION) -> None:
        self.header_name = header_name
        self.precision = precision

    @validate_header_name()
    def test_validate_header_name(self, *args, **kwargs) -> str:
        return "OK"
    
    @validate_precision()
    def test_validate_precision(self, *args, **kwargs) -> str:
        return "OK"

def test_validate_header_name_with_default_value() -> None:
    TC = TestClass()
    result = TC.test_validate_header_name()
    assert result == "OK"

@pytest.mark.parametrize("header_name", [f"valid_header_config_{i:02d}" for i in range(1, 4)])
def test_validate_header_name_with_valid_config(header_name: str, request: pytest.FixtureRequest) -> None:
    header_name = request.getfixturevalue(header_name)
    TC = TestClass(header_name=header_name)
    result = TC.test_validate_header_name()
    assert result == "OK"

@pytest.mark.parametrize("header_name", [f"invalid_header_config_{i:02d}" for i in range(1, 4)])
def test_validate_header_name_with_invalid_config(header_name: str, request: pytest.FixtureRequest) -> None:
    header_name = request.getfixturevalue(header_name)
    with pytest.raises(InvalidHeaderNameException):
        TC = TestClass(header_name=header_name)
        TC.test_validate_header_name()

def test_validate_precision_with_default_value() -> None:
    TC = TestClass()
    result = TC.test_validate_precision()
    assert result == "OK"

@pytest.mark.parametrize("precision", [f"valid_precision_config_{i:02d}" for i in range(1, 4)])
def test_validate_precision_with_valid_config(precision: int, request: pytest.FixtureRequest) -> None:
    precision = request.getfixturevalue(precision)
    TC = TestClass(precision=precision)
    result = TC.test_validate_precision()
    assert result == "OK"

@pytest.mark.parametrize("precision", [f"invalid_precision_config_{i:02d}" for i in range(1, 4)])
def test_validate_precision_with_invalid_config(precision: int, request: pytest.FixtureRequest) -> None:
    precision = request.getfixturevalue(precision)
    with pytest.raises((PrecisionValueOutOfRangeException, TypeError)):
        TC = TestClass(precision=precision)
        TC.test_validate_precision()