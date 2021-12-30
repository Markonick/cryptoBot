FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

EXPOSE 4000

WORKDIR /engine
COPY /engine /engine
COPY ./infra /engine
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD [ "python", "main.py" ]