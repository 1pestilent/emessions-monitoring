FROM python:3.13.1-slim

WORKDIR /app

COPY reqs.txt .

RUN pip install -r reqs.txt

COPY app/ .

CMD ["python", "app.main.py"]