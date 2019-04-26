FROM python:3.7-alpine

WORKDIR /app

COPY requirements.txt .

RUN pip3 install --upgrade pip
RUN pip3 install --upgrade -r requirements.txt

ADD ./src .

CMD ["python3", "server.py"]
