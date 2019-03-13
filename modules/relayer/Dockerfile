FROM python:3.7-alpine

WORKDIR /app

ADD . .

RUN pip3 install -r requirements.txt

CMD ["python3", "src/server.py"]
