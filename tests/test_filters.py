from logging import LogRecord
from asgi_request_duration.filters import RequestDurationFilter
from asgi_request_duration.context import request_duration_ctx_var

# needs to run before the test_request_duration_filter_without_context_value test function
# to ensure the context value is not set before the filter is applied
def test_request_duration_filter_without_context_value(log_record: LogRecord) -> None:
    filter = RequestDurationFilter(default_value="-")
    filter.filter(log_record)
    assert getattr(log_record, request_duration_ctx_var.name) == "-"

def test_request_duration_filter_with_context_value(log_record: LogRecord) -> None:
    request_duration_ctx_var.set("0.123456")
    filter = RequestDurationFilter()
    filter.filter(log_record)
    assert getattr(log_record, request_duration_ctx_var.name) == "0.123456"
