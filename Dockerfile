FROM python:3.8

RUN pip install utmp

WORKDIR /app

ADD src/ ./

RUN mkdir /out

ENTRYPOINT [ "python", "main.py" ]