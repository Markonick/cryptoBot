FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

EXPOSE 6000

COPY . /ticker
COPY ./infra /ticker
WORKDIR /ticker

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD [ "python", "main.py" ]