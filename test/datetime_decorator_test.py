

from datetime import datetime

from app.datetime_decorator import parse_timestamp

def test_parse_timestamp():
    dt = datetime(2019, 12, 31, 11, 59)
    assert parse_timestamp(dt) == '2019-12-31 11:59:00'
