FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

WORKDIR /backtesting
COPY /backtesting /backtesting
COPY ./infra /backtesting
RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir
RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz \
  &&  tar -xzf ta-lib-0.4.0-src.tar.gz \
  &&  rm ta-lib-0.4.0-src.tar.gz \
  && cd ta-lib/ \
  &&  ./configure --prefix=/usr \
  &&  make \
  &&  make install \
  && cd ~ \
  &&  rm -rf ta-lib/ \
  && pip install ta-lib
EXPOSE 8000

# CMD ["python", "main.py"]

CMD ["python", "get_data.py"]