import os

import resend
from dotenv import load_dotenv

load_dotenv()


class EmailService:
    def __init__(self):
        api_key = os.getenv("RESEND_API_KEY")

        if not api_key:
            raise ValueError("RESEND_API_KEY is not set")

        resend.api_key = api_key

        self.from_email = os.getenv(
            "EMAIL_FROM",
            "onboarding@resend.dev",
        )

    def send_email(
        self,
        to: str,
        subject: str,
        body_text: str,
        body_html: str,
    ):
        params = {
            "from": self.from_email,
            "to": [to],
            "subject": subject,
            "text": body_text,
            "html": body_html,
        }

        return resend.Emails.send(params)