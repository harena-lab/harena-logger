FROM python:3.7-alpine

WORKDIR /app

COPY requirements.txt .

RUN pip3 install -U -r requirements.txt

ADD . .

CMD ["python3", "src/server.py"]
