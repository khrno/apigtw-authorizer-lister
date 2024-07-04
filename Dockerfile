FROM python:3.7-slim

WORKDIR /usr/app

ADD ./requirements.txt /usr/app/requirements.txt

RUN pip install -r requirements.txt

ADD . /usr/app/

ENTRYPOINT [ "python", "main.py" ]