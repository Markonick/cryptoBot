FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

EXPOSE 6000

WORKDIR /ticker
COPY /ticker /ticker
COPY ./infra /ticker
RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir
CMD [ "python", "main.py" ]