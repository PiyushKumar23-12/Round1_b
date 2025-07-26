# # Use PyTorch official CPU image with Python 3.9 - adjust py version if needed
# FROM pytorch/pytorch:2.7.1-cuda11.8-cudnn9-runtime

# WORKDIR /app

# COPY requirements.txt .

# RUN pip install --upgrade pip
# RUN pip install --default-timeout=1000 --no-cache-dir -r requirements.txt

# COPY app ./app
# COPY collection ./collection

# ENTRYPOINT ["python", "app/main.py"]


# Start from slim Python image (not full Ubuntu)
FROM python:3.9-slim

# Avoid buffering logs for better Docker logs output
ENV PYTHONUNBUFFERED=1

# Set working directory inside container
WORKDIR /app

# Install system dependencies & clean up in one RUN to reduce image size
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements.txt first to leverage build cache
COPY requirements.txt .

# Upgrade pip and install dependencies, enable retry to avoid flaky downloads
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --default-timeout=1000 --resume-retries=5 -r requirements.txt

# Copy your application source code and data folders
COPY app ./app
COPY collection ./collection

# Set command to run your main.py inside app folder
ENTRYPOINT ["python", "app/main.py"]
