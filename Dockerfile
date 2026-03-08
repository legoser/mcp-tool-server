# Stage 1: Builder
FROM python:3-alpine AS builder

WORKDIR /build

# Install build dependencies for Alpine (minimal)
RUN apk add --no-cache \
    build-base \
    python3-dev \
    libffi-dev

# Copy project files
COPY pyproject.toml requirements.txt ./
COPY src/ ./src/

# Install Python dependencies to a virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -e .

# Stage 2: Runtime
FROM python:3-alpine

WORKDIR /app

# Install only runtime dependencies (curl for health checks)
RUN apk add --no-cache curl

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Copy application code
COPY src/ ./src/
COPY .env* ./

# Set environment variables
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Create non-root user for security
RUN addgroup -g 1000 mcp && \
    adduser -D -u 1000 -G mcp mcp && \
    chown -R mcp:mcp /app

USER mcp

# Expose port for SSE server
EXPOSE 3344

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3344/health || exit 1

# Default command: Run SSE server
CMD ["uvicorn", "src.main_sse:app", "--host", "0.0.0.0", "--port", "3344"]
