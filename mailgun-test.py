import os

import requests

SANDBOX_ID = ""
MAILGUN_SENDING_KEY = ""
MAILGUN_API_URL = f"https://api.mailgun.net/v3/{SANDBOX_ID}.mailgun.org/messages"
FROM_EMAIL_ADDR = f"postmaster@{SANDBOX_ID}.mailgun.org"


def send_simple_message(to_addr: str, subject: str, message: str) -> requests.Response:
    return requests.post(
        MAILGUN_API_URL,
        auth=(
            "api",
            os.getenv("API_KEY", MAILGUN_SENDING_KEY),
        ),
        data={
            "from": FROM_EMAIL_ADDR,
            "to": to_addr,
            "subject": subject,
            "text": message,
        },
    )


print(
    send_simple_message(
        "jonikulov.uz@gmail.com",
        "Hi, Javohir!",
        "Congratulations Javohir, you just sent an email with Mailgun! You are truly awesome!",
    )
)
