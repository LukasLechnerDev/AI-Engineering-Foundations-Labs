# Dockerized project

This is the same AI Engineering Job Agent as in `01-deploy-project`, but now
packaged as a Docker image.

In the previous project we installed Python, `uv` and the dependencies directly
on the EC2 instance. That works, but the server slowly becomes hard to
recreate, and it can behave differently than your laptop. With Docker, the image
contains everything the app needs, so the same artifact runs locally and on the
server.

## What changed from the previous project?

- A `Dockerfile` builds an image with Python, `uv` and the locked dependencies.
- A `.dockerignore` keeps secrets and local files out of the image.
- Configuration is passed into the container as environment variables.
- The container runs as a non-root user.
- The report is written to a mounted folder so it survives the container.

## The Dockerfile explained

- `FROM python:3.12-slim` is a small official Python base image.
- The `uv` binary is copied from the official `uv` image, pinned to one version.
- `pyproject.toml` and `uv.lock` are copied first, then `uv sync --locked`
  installs the exact pinned versions. Docker caches this layer, so changing your
  application code does not reinstall all dependencies.
- The application code is copied afterwards, because it changes most often.
- `PYTHONUNBUFFERED=1` makes log output appear immediately in `docker logs`.
- `UV_PYTHON_DOWNLOADS=never` forbids `uv` from downloading its own Python, so
  the container always runs the Python of the base image.
- `useradd appuser` plus `USER appuser` means the process does not run as root.
- `CMD ["python", "main.py"]` runs the batch workflow once. The container then
  exits. It is not a long-running web server, so we do not expose a port.

## Why a Python base image?

`uv sync` creates a virtual environment, so it is tempting to think we do not
need Python in the base image at all. But a virtual environment does not contain
an interpreter. It contains a `pyvenv.cfg` file that points at a Python
interpreter somewhere else on the system, plus the installed packages.

`uv` can solve that for you: if it finds no suitable interpreter, it downloads a
standalone Python build itself and uses the version from `.python-version`. So
`FROM debian:bookworm-slim` would also work.

We still start from `python:3.12-slim` because it is the simpler option:

- The Python version is visible right in the `FROM` line.
- There is no extra download step during the build.
- The downloaded interpreter would land in the home folder of the build user,
  which our non-root `appuser` may not be able to read.

The image is not meaningfully bigger either. You drop the Python that Debian
ships and add the one `uv` downloaded.

### Keep the version in two places in sync

`.python-version` tells `uv` which Python to use, and the `FROM` line decides
which Python the image actually ships. If you bump `.python-version` to `3.13`,
also change the base image to `python:3.13-slim`.

We copy `.python-version` into the dependency layer and set
`UV_PYTHON_DOWNLOADS=never` exactly for this reason. If the two versions drift
apart, the build stops with a clear error:

```
error: No interpreter found for Python 3.13 in managed installations or search path
```

Without those two lines the mismatch would stay invisible, and you would ship an
image running a different Python version than the one you pinned.

## Secrets stay out of the image

Never copy your `.env` file into the image. Anyone with the image could read it.
`.env` is listed in `.dockerignore`, and the configuration is passed at run time
with `--env-file` instead.

## Build and run locally

Create your local environment file:

```bash
cp .env.example .env
```

Add the required values to `.env`, then build the image:

```bash
docker build -t job-agent:latest .
```

Run the container:

```bash
docker run --rm \
  --env-file .env \
  -v "$(pwd)/report:/app/report" \
  job-agent:latest
```

- `--rm` removes the container after it exits.
- `--env-file .env` passes the configuration as environment variables.
- `-v "$(pwd)/report:/app/report"` mounts the local `report` folder into the
  container, so the generated HTML report ends up on your machine.

The report is written to `report/job-agent-report.html`.

To email the report, set `SEND_EMAIL=true` and configure the Resend values shown
in `.env.example`. Leave `JOB_AGENT_SENDER_EMAIL` commented out to use the
default Resend test sender.

## Useful Docker commands

```bash
docker images                               # list your local images
docker ps -a                                # list containers, also exited ones
docker logs <container-id>                  # show the output of a container
docker run --rm -it job-agent:latest bash   # open a shell inside the image
```

A container that finished successfully has exit code `0`. You can check it with
`docker ps -a`, or with `echo $?` right after the run.

## Deploy on AWS EC2

### 1. Create and secure the instance

- Create an Ubuntu EC2 instance.
- Allow inbound SSH traffic only from your own IP address.
- Do not open an application port. This project is a batch workflow, not a web
  server.

### 2. Connect and install Docker

Connect to the instance with SSH, then install Git and Docker:

```bash
sudo apt update
sudo apt install --yes git docker.io
sudo usermod --append --groups docker $USER
```

Log out and back in, so the new group membership takes effect.

### 3. Clone and configure the project

```bash
git clone <repository-url>
cd AI-Engineering-Foundations-Labs/4-deployment-on-aws/02-dockerized-project
cp .env.example .env
```

Add the required secrets and configuration to `.env`. Never commit this file.

### 4. Build and run

```bash
docker build -t job-agent:latest .
docker run --rm --env-file .env -v "$(pwd)/report:/app/report" job-agent:latest
```

The deployment is successful when the container exits with code `0` and the
report is generated or delivered by email.

Note that we still build the image on the server here. Building the image once
in a pipeline and only pulling it on the server is the next step, and that is
what the CI/CD lesson covers.
