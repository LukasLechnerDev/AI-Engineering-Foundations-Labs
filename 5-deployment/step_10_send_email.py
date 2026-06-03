import os

import resend


def send_email(html: str) -> None:
    print("\nStep 10: Sending email digest...")
    resend.api_key = os.environ["RESEND_API_KEY"]
    recipient = os.environ["DIGEST_RECIPIENT_EMAIL"]

    response = resend.Emails.send(
        {
            "from": "AI Engineer Digest <onboarding@resend.dev>",
            "to": [recipient],
            "subject": "Your Daily AI Engineer Job Digest",
            "html": html,
        }
    )
    print(f"  Email sent! ID: {response['id']}")
