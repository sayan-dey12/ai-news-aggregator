import os

import resend
from dotenv import load_dotenv


load_dotenv()

resend.api_key = os.getenv("RESEND_API_KEY")


params = {
    "from": "AI News Aggregator <onboarding@resend.dev>",
    "to": ["sayandey.dev@gmail.com"],
    "subject": "AI News Aggregator - Test Email",
    "html": """
        <h1>Hello!</h1>
        <p>This is a test email from the AI News Aggregator.</p>
        <p>Resend integration is working.</p>
    """,
}


email = resend.Emails.send(params)

print(email)