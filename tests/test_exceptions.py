from asgi_request_duration.exceptions import InvalidHeaderNameException, PrecisionValueOutOfRangeException

def test_invalid_header_name_exception() -> None:
    header_name = "Invalid Header"
    exception = InvalidHeaderNameException(header_name)
    assert str(exception) == f"{header_name} - ('{InvalidHeaderNameException.description}',)"

def test_precision_value_out_of_range_exception() -> None:
    precision = 20
    min_value = 0
    max_value = 17
    exception = PrecisionValueOutOfRangeException(precision, min_value, max_value)
    assert str(exception) == f"{precision} - ('{PrecisionValueOutOfRangeException.description}',) (Allowed range: {min_value}-{max_value})"