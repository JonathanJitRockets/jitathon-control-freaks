FROM ubuntu:22.04

RUN apt-get update && apt-get install -y git python3

WORKDIR /code

COPY gitleaks /usr/local/bin/
COPY gitleaks_wrapper.py .

CMD ["python3", "gitleaks_wrapper.py"]