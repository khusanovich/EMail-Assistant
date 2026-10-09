FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files
COPY pyproject.toml ./

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir .

# Copy application code
COPY app/ ./app/
COPY scripts/ ./scripts/
COPY dashboard/ ./dashboard/
COPY alembic.ini ./

# Create non-root user
RUN useradd -m -u 1000 jobmail && \
    chown -R jobmail:jobmail /app

USER jobmail

# Expose ports
EXPOSE 8000 8501

# Default command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
