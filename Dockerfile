FROM python:3.7.3

COPY . .
WORKDIR .

RUN pip install -r requirements.txt

CMD ["python3", "./fifa_data/fifa_data/spiders/test_spider.py"]