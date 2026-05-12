import os

import resend
from dotenv import load_dotenv

load_dotenv()

resend.api_key = os.environ["RESEND_API_KEY"]

params: resend.Emails.SendParams = {
    "from": "Acme <onboarding@resend.dev>",
    "to": ["office@lukaslechner.com"],
    "subject": "hello world",
    "html": "<p>it works!</p>",
}

email = resend.Emails.send(params)
print(email)
