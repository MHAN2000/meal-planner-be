#app/.dockerfile
# Stage 1: Build Stage (uses a slim Python image for smaller final image size)
FROM python:3.10-slim-buster AS builder

# Set the working directory inside the container
WORKDIR /app

# Install build dependencies (needed for some Python packages like psycopg2)
# These will NOT be in the final image, only for building wheels.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements.txt first to leverage Docker cache
# This speeds up builds if requirements.txt doesn't change
COPY requirements.txt .

# Install Python dependencies
# Using --no-cache-dir to avoid caching pip packages in the builder stage
# Using --user to install packages into a user-specific directory (good practice for multi-stage builds)
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Final Image Stage (uses a fresh, even smaller slim Python image)
FROM python:3.10-slim-buster

# Set environment variables for the application
# This is crucial for uvicorn and other services
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Set the working directory again for the final image
WORKDIR /app

# Copy the installed packages from the builder stage
# This copies only the *installed* packages, not the build tools
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy the actual application code
COPY ./app /app/app

COPY alembic.ini .
COPY alembic /app/alembic

# If your main.py is directly in /app, adjust this: COPY ./main.py /app/main.py

# Expose the port your FastAPI application will run on
EXPOSE 8000

# Command to run the application using Uvicorn
# --host 0.0.0.0 makes the server accessible from outside the container
# --port 8000 specifies the port
# app.main:app refers to 'app' directory, 'main.py' module, and 'app' FastAPI instance
# CMD ["uvicorn", "app.main:app", "--host", "0.0.00", "--port", "8000"]