FROM python:3.10-slim

WORKDIR /code

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

RUN pip install flake8

COPY ./app ./app
COPY .flake8 .flake8

EXPOSE 8000

CMD ["sh", "-c", "python app/core/management/wait_for_db.py && uvicorn app.main:app --host 0.0.0.0 --port 8000"]