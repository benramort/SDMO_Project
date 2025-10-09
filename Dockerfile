FROM python:3.13
WORKDIR /app
COPY requirements.txt .
RUN apt-get update && apt-get install -y git build-essential
RUN pip install -r requirements.txt
RUN pip install -U pytest
