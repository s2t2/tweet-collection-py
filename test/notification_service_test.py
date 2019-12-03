

from app.notification_service import recipient_emails #, message_compilation

def test_recipient_emails():
    assert recipient_emails(" hello@me.com, there@you.org ") == ['hello@me.com', 'there@you.org']

def test_message_compilation():
    err = RuntimeError("OOPS")
    contents = f"{type(err)}<br>{err}"
    assert contents == "<class 'RuntimeError'><br>OOPS"

    status_code = 202
    contents = f"{type(status_code)}<br>{status_code}"
    assert contents == "<class 'int'><br>202"
