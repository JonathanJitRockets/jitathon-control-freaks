FROM ubuntu:22.04
RUN apt-get update && apt-get install -y git
COPY gitleaks /usr/local/bin/gitleaks
RUN chmod +x /usr/local/bin/gitleaks
CMD ["gitleaks", "detect", "--verbose", "--report-format=json", "--report-path=/tmp/gitleaks-report.json", "--source=/code", "--no-git"]