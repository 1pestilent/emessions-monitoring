FROM python:3.13.1-slim

RUN pip install poetry

WORKDIR /app .

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \ 
    && poetry install

COPY . .

CMD ["python", "app.main.py"]

