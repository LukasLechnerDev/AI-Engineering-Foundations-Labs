# Small official Python base image
FROM python:3.12-slim

# Copy the uv binary from the official uv image (pinned to one version)
COPY --from=ghcr.io/astral-sh/uv:0.11.7 /uv /usr/local/bin/uv

# Print logs immediately instead of buffering them
ENV PYTHONUNBUFFERED=1

# Always use the Python of the base image.
# If .python-version does not match it, the build fails instead of quietly
# downloading a different Python version.
ENV UV_PYTHON_DOWNLOADS=never

WORKDIR /app

# Install the locked dependencies first.
# Docker caches this layer as long as these three files do not change.
COPY pyproject.toml uv.lock .python-version ./
RUN uv sync --locked

# Use the virtual environment that uv just created
ENV PATH="/app/.venv/bin:$PATH"

# Copy the application code
COPY . .

# Run as a non-root user instead of root
RUN useradd --create-home appuser && chown -R appuser:appuser /app
USER appuser

# The container runs the batch workflow once and then exits
CMD ["python", "main.py"]
