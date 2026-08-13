FROM python:3.11-alpine

RUN apk add --no-cache socat

WORKDIR /app
COPY chall.py .

RUN adduser -D -u 1000 ctf
USER 1000

EXPOSE 1337
CMD ["socat", "TCP-LISTEN:1337,reuseaddr,fork", "EXEC:python3 /app/chall.py"]
