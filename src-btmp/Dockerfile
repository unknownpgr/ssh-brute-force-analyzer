FROM python:3.8

RUN pip install utmp

WORKDIR /app

ADD ./ ./

RUN mkdir /out

ENTRYPOINT [ "sh", "init.sh" ]