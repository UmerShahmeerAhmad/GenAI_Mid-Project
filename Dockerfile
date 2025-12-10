# ----------------------------
# Dockerfile for AI-CODE-REVIEWER
# ----------------------------
FROM python:3.11-slim

# Set metadata
LABEL maintainer="UmerShahmeerAhmad"
LABEL description="AI Code Reviewer - A Flask application for reviewing code using AI providers"

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /app

# Create non-root user for security
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port used by Flask app
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/').read()"

# Default command: run Flask app
CMD ["python", "app.py"]
