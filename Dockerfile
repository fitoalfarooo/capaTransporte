FROM alpine:3.10

WORKDIR /app

COPY requirements.txt .

RUN apk add --no-cache python3-dev && pip3 install --upgrade pip

RUN pip install -r requirements.txt

RUN apk add --no-cache ffmpeg

COPY . .

EXPOSE 5050

ENTRYPOINT [ "python3","-u","server.py" ]