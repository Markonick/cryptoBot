FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

WORKDIR /backtesting
COPY /backtesting /backtesting
COPY ./infra /backtesting
RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir

EXPOSE 8000

CMD ["python", "main.py"]