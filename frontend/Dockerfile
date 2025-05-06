# Use official Python base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create working directory
WORKDIR /app

# Install system dependencies (optional: audio, fonts, etc.)
RUN apt-get update && apt-get install -y \
    ffmpeg libsm6 libxext6 curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file and install dependencies
COPY requirements-app.txt .
RUN pip install --no-cache-dir -r requirements-app.txt

# Copy your frontend app code
COPY . .

# Expose Gradio's default port
EXPOSE 7860

# Command to run your Gradio app
CMD ["python", "main.py"]
