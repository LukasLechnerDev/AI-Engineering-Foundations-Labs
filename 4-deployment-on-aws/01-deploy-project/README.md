# Deploy project

This is the completed AI Engineering Job Agent from the previous modules,
prepared for its first manual deployment on an AWS EC2 instance.

This project intentionally does not use Docker, cron, or CI/CD yet. The goal is
to experience the manual deployment steps before introducing the tools that
make deployments more reproducible and easier to operate.

## What changed from the previous project?

- Raw JSON schemas were replaced with Pydantic models.
- The OpenAI calls now use `responses.parse()` and `output_parsed`.
- `.env.example` documents the required configuration.
- Local secrets and the generated report are excluded from Git.
- Environment variables take precedence over values from `.env`.

## Run locally

Create your local environment file:

```bash
cp .env.example .env
```

Add the required values to `.env`, then install the locked dependencies and run
the workflow:

```bash
uv sync --locked
uv run python main.py
```

The app writes the HTML report to `report/job-agent-report.html`.

To email the report, set `SEND_EMAIL=true` and configure the Resend values shown
in `.env.example`. Leave `JOB_AGENT_SENDER_EMAIL` commented out to use the
default Resend test sender.

## Deploy manually on AWS EC2

### 1. Create and secure the instance

- Create an Ubuntu EC2 instance.
- Allow inbound SSH traffic only from your own IP address.
- Do not open an application port. This project is a batch workflow, not a web
  server.

### 2. Connect and install the tools

Connect to the instance with SSH, then install Git and `uv`:

```bash
sudo apt update
sudo apt install --yes git curl
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.local/bin/env
```

### 3. Clone and configure the project

```bash
git clone <repository-url>
cd AI-Engineering-Foundations-Labs/4-deployment-on-aws/01-deploy-project
cp .env.example .env
```

Add the required secrets and configuration to `.env`. Never commit this file.

### 4. Install and run

```bash
uv sync --locked
uv run python main.py
```

The first deployment is successful when the workflow completes and the report
is generated or delivered by email.
