# Synchronous version
FROM ubuntu:20.04

COPY requirements.txt /tmp/

RUN apt-get update \
    && apt-get install -y --no-install-recommends python3-opcua python3 \
    && rm -rf /var/lib/apt/lists/*

RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser

COPY src/SyncOPCUA.py .

ENTRYPOINT [ "python3", "./SyncOPCUA.py" ]