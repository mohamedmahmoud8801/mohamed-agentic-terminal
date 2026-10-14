FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_CACHE_DIR=/root/.cache/uv

WORKDIR /app

# Install uv and uvx
RUN pip install --no-cache-dir uv

# Install the Gateway's direct runtime dependency
RUN pip install --no-cache-dir "fastmcp>=3.2.4,<4.0.0"

# Copy the Gateway
COPY mcp_app/gateway.py /app/gateway.py

EXPOSE 8001

CMD ["python", "gateway.py"]