# Build stage
FROM python:3.11.11-alpine as builder

# Set working directory
WORKDIR /app

# Install build dependencies
RUN apk add --no-cache \
    build-base \
    curl

# Install Python dependencies
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Final stage
FROM python:3.11.11-alpine

# Create non-root user
RUN adduser -D pokemon

# Set working directory
WORKDIR /app

# Update package repositories and install Chromium and Chromedriver
RUN apk add --update --no-cache \
    chromium \
    chromium-chromedriver

# Install runtime dependencies
RUN apk add --no-cache \
    curl

# Copy wheels from builder
COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache /wheels/*

# Copy application code
COPY --chown=pokemon:pokemon . .

# Create data directory with correct permissions
RUN mkdir -p /app/data && chown pokemon:pokemon /app/data && chmod 777 /app/data

# Switch to non-root user
USER pokemon

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/health || exit 1

# Expose port
EXPOSE 8000

# Set environment variables
ENV HOST=0.0.0.0 \
    PORT=8000 \
    CHROMEDRIVER_PATH=/usr/bin/chromedriver \
    PATH="/usr/bin/chromedriver:${PATH}"

# Run the application
CMD ["python", "main.py"]