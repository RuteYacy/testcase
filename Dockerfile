FROM python:3.10-slim

WORKDIR /code

COPY ./app/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

EXPOSE 8000

CMD ["sh", "-c", "python app/core/management/wait_for_db.py && uvicorn app.main:app --host 0.0.0.0 --port 8000"]