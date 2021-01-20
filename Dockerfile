FROM python:3.7-alpine

WORKDIR /app

COPY requirements.txt .

RUN touch /var/log/harena-logger.log
RUN chmod 755 /var/log/harena-logger.log
RUN pip3 install --upgrade pip
RUN pip3 install --upgrade -r requirements.txt

ADD ./src .

CMD ["python3", "-u", "server.py"]
