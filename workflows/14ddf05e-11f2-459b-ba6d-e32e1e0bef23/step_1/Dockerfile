FROM ubuntu:22.04

RUN apt-get update && apt-get install -y git

WORKDIR /code

COPY gitleaks /usr/local/bin/

CMD ["gitleaks", "detect", "--verbose", "--report-format=json", "--report-path=/tmp/gitleaks-report.json", "--source=/code", "--no-git"]