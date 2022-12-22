FROM python:3.8

RUN pip install paramiko

WORKDIR /app

ADD ./ ./

RUN mkdir /out

ENTRYPOINT [ "python", "main.py" ]