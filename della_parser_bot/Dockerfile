FROM python:3.10-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt


COPY . ./della_parser_bot
CMD ["celery", "-A", "della_parser_bot", "worker", "-B", "-E", "--loglevel=info"]