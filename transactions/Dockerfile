FROM python:3.9


WORKDIR /transactions
COPY /transactions /transactions
RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir
EXPOSE 7000

CMD ["python", "main.py"]