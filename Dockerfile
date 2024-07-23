FROM python:latest

WORKDIR /code

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY .venv/crud.py /code
COPY .venv/main.py /code
COPY .venv/models.py /code
COPY /templates /code/templates


ENTRYPOINT ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0"]
