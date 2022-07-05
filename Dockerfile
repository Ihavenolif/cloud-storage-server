FROM python:3.10.4-alpine

EXPOSE 5000/tcp

WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY app.py .

CMD [ "python3", "./app.py" ]