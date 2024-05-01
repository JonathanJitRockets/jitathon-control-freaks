FROM ubuntu:22.04

# Install necessary packages
RUN apt-get update && apt-get install -y git

# Copy Gitleaks executable
COPY gitleaks /usr/bin/gitleaks

# Set work directory and permissions for gitleaks
WORKDIR /app
RUN chmod +x /usr/bin/gitleaks

# Set up entry point
ENTRYPOINT ["gitleaks", "detect", "--verbose", "--no-git", "--report-format=json", "--report-path=/tmp/gitleaks-report.json", "--source=/app"]