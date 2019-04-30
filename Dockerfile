FROM python:3.7.3

COPY . .
WORKDIR .

RUN pip install -r requirements.txt
