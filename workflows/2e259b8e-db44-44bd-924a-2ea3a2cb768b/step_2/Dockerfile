FROM ubuntu:22.04

# Install necessary packages
RUN apt-get update && apt-get install -y git python3

# Copy Gitleaks executable
COPY gitleaks /usr/bin/gitleaks

# Copy Python script
COPY example.py /app/example.py

# Set work directory and permissions for gitleaks
WORKDIR /app
RUN chmod +x /usr/bin/gitleaks

# Set up entry point
ENTRYPOINT ["python3", "example.py"]