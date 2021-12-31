FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

EXPOSE 4000

WORKDIR /engine
COPY /engine /engine
COPY ./infra /engine
RUN apt-get update
RUN apt-get install libx11-dev
RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir
CMD [ "python", "main.py" ]