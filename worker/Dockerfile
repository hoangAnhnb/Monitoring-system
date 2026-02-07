FROM python:3.11

WORKDIR /worker
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY worker.py .

CMD ["celery", "-A", "worker", "worker", "--loglevel=info"]
