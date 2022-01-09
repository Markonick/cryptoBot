FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

EXPOSE 4000

WORKDIR /engine
COPY /engine /engine
COPY ./infra /engine
RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir

EXPOSE 8000

CMD ["uvicorn", "main:engine", "--reload", "--host", "0.0.0.0", "--port", "8000"]