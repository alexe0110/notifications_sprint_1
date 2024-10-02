FROM python:3.12

WORKDIR /opt/app/notifications

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN apt update && pip install --upgrade pip
COPY pyproject.toml poetry.lock /opt/app/notifications/

RUN pip install --no-compile poetry \
 && poetry config virtualenvs.create false \
 && poetry install --no-interaction --no-ansi


COPY . .

EXPOSE 8000

CMD ["gunicorn", "main:app", "-w", "4", "-k", "uvicorn_worker.UvicornWorker", "--bind", "0.0.0.0:8000"]