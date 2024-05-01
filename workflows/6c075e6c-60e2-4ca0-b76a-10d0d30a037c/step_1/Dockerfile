# Use Ubuntu 22.04 as base image
FROM ubuntu:22.04

# Update and install required tools
RUN apt-get update && apt-get install -y \
    git \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy the gitleaks executable into the image
COPY gitleaks /usr/bin/gitleaks

# Make sure the binary is executable
RUN chmod +x /usr/bin/gitleaks

# Set working directory to /code
WORKDIR /code

# Command to run when the container starts
CMD ["gitleaks", "detect", "--verbose", "--report-format=json", "--report-path=/tmp/gitleaks-report.json", "--source=/code", "--no-git"]