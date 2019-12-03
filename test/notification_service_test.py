

from app.notification_service import admin_emails

def test_admin_emails():
    assert admin_emails(" hello@me.com, there@you.org ") == ['hello@me.com', 'there@you.org']
