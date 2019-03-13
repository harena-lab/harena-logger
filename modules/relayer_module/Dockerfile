FROM ubuntu:18.04

RUN apt update 
RUN apt install -y python3 python3-pip htop 

WORKDIR  /usr/app

ADD . .

RUN pip3 install -r requirements.txt


CMD ["python3", "src/server.py"]