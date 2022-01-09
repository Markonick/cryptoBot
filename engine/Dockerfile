FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

WORKDIR /engine
COPY /engine /engine
COPY ./infra /engine
RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir

EXPOSE 8000

CMD ["python", "main.py"]