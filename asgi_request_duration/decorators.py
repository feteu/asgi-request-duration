from asgi_request_duration.exceptions import InvalidHeaderNameException, PrecisionValueOutOfRangeException
from asgi_request_duration.constants import (
    _DEFAULT_HEADER_NAME,
    _DEFAULT_PRECISION,
    _DEFAULT_SKIP_VALIDATE_HEADER_NAME,
    _DEFAULT_SKIP_VALIDATE_PRECISION,
    _HEADER_NAME_PATTERN,
    _PRECISION_MAX,
    _PRECISION_MIN,
)

def validate_header_name(skip: bool =_DEFAULT_SKIP_VALIDATE_HEADER_NAME) -> callable:
    """
    Decorator to validate the header name against a pattern.
    
    Args:
        func (function): The function to be decorated.
        skip (bool): Flag to skip the validation.
    
    Returns:
        function: The wrapped function with header name validation.
    
    Raises:
        InvalidHeaderNameException: If the header name is invalid.
    """
    def decorator(func: callable)-> callable:
        def wrapper(*args, **kwargs) -> callable:
            if not skip:
                header_name = kwargs.get('header_name', _DEFAULT_HEADER_NAME)
                if not _HEADER_NAME_PATTERN.match(header_name):
                    raise InvalidHeaderNameException(header_name)
            return func(*args, **kwargs)
        return wrapper
    return decorator

def validate_precision(skip: bool =_DEFAULT_SKIP_VALIDATE_PRECISION)-> callable:
    """
    Decorator to validate the precision value.
    
    Args:
        func (function): The function to be decorated.
        skip (bool): Flag to skip the validation.
    
    Returns:
        function: The wrapped function with precision validation.
    
    Raises:
        PrecisionValueOutOfRangeException: If the precision value is out of range.
    """
    def decorator(func: callable) -> callable:
        def wrapper(*args, **kwargs) -> callable:
            if not skip:
                precision = kwargs.get('precision', _DEFAULT_PRECISION)
                if not (_PRECISION_MIN <= precision <= _PRECISION_MAX):
                    raise PrecisionValueOutOfRangeException(precision, _PRECISION_MIN, _PRECISION_MAX)
            return func(*args, **kwargs)
        return wrapper
    return decorator