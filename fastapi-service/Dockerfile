FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY ./app /app

RUN pip install boto3

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]
