
from datetime import datetime
import os
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from app import APP_ENV

load_dotenv()

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", default="OOPS")
FROM_EMAIL = os.getenv("FROM_EMAIL", default="OOPS")
TO_EMAILS = os.getenv("TO_EMAILS", default="HELLO, THERE")

def recipient_emails(emails_csv_str=TO_EMAILS):
    return [email.strip() for email in emails_csv_str.split(",")]

def email_client():
    client = SendGridAPIClient(SENDGRID_API_KEY) #> <class 'sendgrid.sendgrid.SendGridAPIClient>
    print("EMAIL CLIENT:", type(client))
    return client

def send_email(subject, contents):
    subject += f" [env:{APP_ENV}]"
    contents += f"<br>Sent at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    to_emails = recipient_emails()
    print("SENDING EMAIL FROM:", FROM_EMAIL)
    print("SENDING EMAIL TO:", to_emails)

    message = Mail(from_email=FROM_EMAIL, to_emails=to_emails, subject=subject, html_content=contents)
    try:
        response = email_client().send(message)
        print("EMAIL RESPONSE:", type(response)) #> <class 'python_http_client.client.Response'>
        print(response.status_code) #> 202 indicates SUCCESS
        print(response.body)
        print(response.headers)
    except Exception as e:
        print("EMAIL ERROR:", e.message)

if __name__ == "__main__":

    send_email(subject="Testing 123", contents="Testing the Notification Service")
