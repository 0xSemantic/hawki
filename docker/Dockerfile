# --------------------
# File: docker/Dockerfile
# --------------------
# Multi‑stage build for Hawk-i CLI

# ---- Builder stage ----
FROM python:3.11-slim AS builder

WORKDIR /build

# Copy only dependency files first for better caching
COPY pyproject.toml requirements.txt README.md ./
COPY hawki/ ./hawki/
COPY cli/ ./cli/
COPY scripts/ ./scripts/

# Build wheel
RUN pip install --upgrade pip build && \
    python -m build --wheel

# ---- Final stage ----
FROM python:3.11-slim

# Install runtime dependencies (no build tools needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create a non‑root user
RUN useradd --create-home hawki
WORKDIR /home/hawki

# Copy the wheel from builder
COPY --from=builder /build/dist/*.whl /tmp/

# Install the wheel and its dependencies
RUN pip install --no-cache-dir /tmp/*.whl && \
    rm /tmp/*.whl

# Ensure the hawki command is available
USER hawki

ENTRYPOINT ["hawki"]
CMD ["--help"]