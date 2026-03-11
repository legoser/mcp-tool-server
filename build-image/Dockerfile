FROM python:3.13-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV PATH="/home/runner/.local/bin:${PATH}"

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    docker.io \
    nodejs \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir ruff pytest pytest-asyncio

RUN useradd -m runner && usermod -aG docker runner

USER runner
