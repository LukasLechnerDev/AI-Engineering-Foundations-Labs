# Full portfolio project

Run the report locally with:

```bash
uv run python main.py
```

The app writes the HTML report to `report/job-agent-report.html`.

To email the report, set these values in `.env`:

```bash
SEND_EMAIL=true
RESEND_API_KEY=your_resend_api_key
JOB_AGENT_RECIPIENT_EMAIL=your_email@example.com
```

Optionally set `JOB_AGENT_SENDER_EMAIL` if you have verified your own sending domain in Resend.

Set `SEND_EMAIL=false` if HTML rendering should be the last step.
