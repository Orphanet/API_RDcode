FROM python:3.8-alpine

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY ./requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY ./swagger_server/ ./swagger_server/

WORKDIR /usr/src/app/swagger_server

ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app"

EXPOSE 8080

ENTRYPOINT ["python3"]

CMD ["./API_main.py"]