FROM python:3.8-slim

WORKDIR /foot_bot

COPY requirements.txt /foot_bot/
RUN pip install -r /foot_bot/requirements.txt
COPY . /foot_bot/

CMD python3 /foot_bot/app.py