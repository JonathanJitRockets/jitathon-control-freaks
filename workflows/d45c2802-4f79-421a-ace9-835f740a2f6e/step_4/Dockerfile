FROM ubuntu:22.04

RUN apt-get update && apt-get install -y python3 python3-pip git && rm -rf /var/lib/apt/lists/*
RUN pip3 install pydantic

# Creating necessary directories
RUN mkdir /code

# Copying binaries
COPY entrypoint /usr/bin/entrypoint
COPY gitleaks /usr/bin/gitleaks
RUN chmod +x /usr/bin/gitleaks
RUN chmod +x /usr/bin/entrypoint

# Copy Python script
COPY run_gitleaks.py /app/run_gitleaks.py

# Setting work directory
WORKDIR /app

# Environment variable for output file
ENV SECURITY_CONTROL_OUTPUT_FILE /tmp/jit_output.json

# Setting entrypoint
ENTRYPOINT ["/usr/bin/entrypoint", "python3", "/app/run_gitleaks.py"]