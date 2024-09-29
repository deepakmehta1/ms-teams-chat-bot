FROM python:3.12-slim

WORKDIR /app

RUN pip install --upgrade pip && pip install poetry

COPY pyproject.toml poetry.lock* /app/

RUN poetry config virtualenvs.create false && poetry install --no-dev

COPY . /app

EXPOSE 3978

CMD ["python3", "app.py"]
