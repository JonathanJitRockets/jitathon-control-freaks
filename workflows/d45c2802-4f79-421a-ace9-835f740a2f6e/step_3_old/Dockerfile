FROM ubuntu:22.04

RUN apt-get update && apt-get install -y python3 python3-pip && rm -rf /var/lib/apt/lists/*

RUN pip3 install pydantic

COPY gitleaks /usr/bin/gitleaks 
RUN chmod +x /usr/bin/gitleaks

COPY run_gitleaks.py /app/run_gitleaks.py

WORKDIR /app
ENTRYPOINT ["python3", "run_gitleaks.py"]
