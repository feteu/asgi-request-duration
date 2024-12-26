import pytest
from asgi_request_duration.decorators import validate_header_name, validate_precision
from asgi_request_duration.exceptions import InvalidHeaderNameException, PrecisionValueOutOfRangeException

@validate_header_name()
def dummy_function_with_header_name(header_name: str = None) -> str:
    return header_name

@validate_precision()
def dummy_function_with_precision(precision: int = None) -> int:
    return precision

def test_validate_header_name_valid() -> None:
    assert dummy_function_with_header_name(header_name="Valid-Header") == "Valid-Header"

def test_validate_header_name_invalid() -> None:
    with pytest.raises(InvalidHeaderNameException):
        dummy_function_with_header_name(header_name="Invalid Header")

def test_validate_precision_valid() -> None:
    assert dummy_function_with_precision(precision=5) == 5

def test_validate_precision_invalid() -> None:
    with pytest.raises(PrecisionValueOutOfRangeException):
        dummy_function_with_precision(precision=20)