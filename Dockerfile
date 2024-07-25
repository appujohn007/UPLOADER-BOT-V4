# Use the official Python image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libssl-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the dependencies file to the working directory
COPY needs.txt .

# Install any needed dependencies specified in needs.txt
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r needs.txt

# Copy the rest of the application code to the working directory
COPY . .

# Command to run the application
CMD ["python", "bot.py"]
