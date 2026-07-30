# Deploy project

This is the completed AI Engineering Job Agent from the previous modules,
prepared for its first manual deployment on an AWS EC2 instance.

This project can be deployed manually to experience the individual deployment
steps. It also includes a Dockerfile and a GitHub Actions workflow that builds
the image and publishes it to Amazon ECR.

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

The job search can be configured in `.env` or with exported environment
variables:

```dotenv
SITE_NAME=linkedin,indeed
LOCATION=USA
COUNTRY_INDEED=USA
JOB_TYPE=fulltime
HOURS_OLD=72
RESULTS_WANTED=10
```

You can override any of these values for one run with CLI arguments:

```bash
uv run python main.py \
  --site-name linkedin indeed \
  --location "New York, NY" \
  --country-indeed USA \
  --job-type fulltime \
  --hours-old 24 \
  --results-wanted 20
```

CLI arguments take precedence over exported environment variables, which take
precedence over values in `.env`. The underscore forms, such as `--site_name`
and `--results_wanted`, are also supported.

To email the report, set `SEND_EMAIL=true` and configure the Resend values shown
in `.env.example`. Leave `JOB_AGENT_SENDER_EMAIL` commented out to use the
default Resend test sender.

## Build and publish with GitHub Actions

The GitHub Actions workflow builds the Docker image and publishes it to Amazon
ECR whenever relevant changes are pushed to `main`. It can also be started
manually from the Actions tab.

In the GitHub repository, open **Settings → Secrets and variables → Actions →
Variables** and add these repository variables:

- `AWS_REGION`: AWS Region containing the ECR repository, for example
  `eu-north-1`.
- `AWS_ROLE_ARN`: ARN of the IAM role that GitHub Actions can assume through
  OpenID Connect (OIDC).
- `ECR_REPOSITORY`: ECR repository name only, for example `ai-job-agent`. Do not
  enter the full repository URI.

These values configure the GitHub Actions runner and do not belong in the
project's local `.env` file. The workflow obtains the AWS account-specific ECR
registry address automatically after authentication.

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
