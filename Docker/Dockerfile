FROM python:3.9.10

COPY ../Binance /opt/binancelistings
WORKDIR /opt/binancelistings
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "ieomoon.py"]