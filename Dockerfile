FROM python:3.11.1-bullseye

ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
