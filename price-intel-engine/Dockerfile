# Use slim image for smaller footprint
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Set env variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies (if any needed for curl_cffi or others)
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project code
COPY . .

# Create volume/directory for config if needed (though we encourage env vars)
# config/ folder is copied, but we might mount credentials at runtime

# Default command (can be overridden)
# Example usage: docker run price-intel --term "Butter"
ENTRYPOINT ["python", "src/main.py"]
