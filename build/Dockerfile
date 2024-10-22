FROM python:3.8-alpine

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY ./requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY ./media/ ./media/
COPY ./swagger_server/ ./swagger_server/

WORKDIR /usr/src/app/swagger_server

ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app"

EXPOSE 8080

ENTRYPOINT ["python3"]

CMD ["./API_main.py"]

# Build with:
# docker build -t api_rdcode:{ver} . --label api_rdcode:{ver}

# Run with:
# docker run -p 8080:8080 --name api_rdcode_{ver} api_rdcode:{ver}

# Export with:
# docker save api_rdcode:{ver} -o ./api_rdcode_{ver}

# Load with:
# docker load -i {path}\api_rdcode_{ver}