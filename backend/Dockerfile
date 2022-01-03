FROM python:3.9


WORKDIR /backend
COPY /backend /backend
COPY ./infra /backend
RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir
EXPOSE 8000

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]