import os
from pathlib import Path

import resend
from langfuse import observe

DEFAULT_SENDER_EMAIL = "AI Engineering Job Report <onboarding@resend.dev>"
SUBJECT = "Your AI Engineering Job Report"


class EmailStep:
    @observe(name="send-email", as_type="tool")
    def run(self, report_path):
        print("\n--- Step 7: Sending email report ---")

        recipient_email = os.environ.get("JOB_AGENT_RECIPIENT_EMAIL")
        if not recipient_email:
            raise ValueError(
                "JOB_AGENT_RECIPIENT_EMAIL is missing from your .env file."
            )

        resend_api_key = os.environ.get("RESEND_API_KEY")
        if not resend_api_key:
            raise ValueError("RESEND_API_KEY is missing from your .env file.")

        resend.api_key = resend_api_key

        html = Path(report_path).read_text(encoding="utf-8")
        params: resend.Emails.SendParams = {
            "from": os.environ.get("JOB_AGENT_SENDER_EMAIL", DEFAULT_SENDER_EMAIL),
            "to": [recipient_email],
            "subject": SUBJECT,
            "html": html,
        }

        email = resend.Emails.send(params)
        print(f"Sent report to {recipient_email}. Email id: {email['id']}")
