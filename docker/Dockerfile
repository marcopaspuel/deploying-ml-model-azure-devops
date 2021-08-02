FROM python:3.8.6-slim as builder

# Install requirements
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Copy source code
COPY src /server/src/
WORKDIR /server

ENTRYPOINT ["python", "-m", "src.server"]
