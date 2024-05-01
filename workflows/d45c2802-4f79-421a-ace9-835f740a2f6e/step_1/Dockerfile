FROM ubuntu:22.04

RUN apt-get update && apt-get install -y ca-certificates && rm -rf /var/lib/apt/lists/*
COPY gitleaks /usr/bin/gitleaks
RUN chmod +x /usr/bin/gitleaks
WORKDIR /app
ENTRYPOINT ["gitleaks", "detect", "--verbose", "--report-format=json", "--report-path=/tmp/gitleaks-report.json", "--source=/code", "--no-git"]