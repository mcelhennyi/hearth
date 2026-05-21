# Hearth Docker profile: runtime deps in the image; plugin tree bind-mounted at /app.
FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    HEARTH_VAR_DIR=/var/hearth

COPY pyproject.toml .
RUN pip install --no-cache-dir \
    "fastapi>=0.110" \
    "uvicorn[standard]>=0.29"

EXPOSE 8201

CMD ["sh", "-c", "exec uvicorn {{ python_package }}.app:create_app --factory --host 0.0.0.0 --port \"${HEARTH_PLUGIN_PORT:-8201}\""]
