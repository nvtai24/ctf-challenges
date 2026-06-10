FROM python:3.11-slim

RUN apt-get update && apt-get install -y socat && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY chall.py .

RUN useradd -m -u 1000 ctf
USER 1000

EXPOSE 1337
CMD ["socat", "TCP-LISTEN:1337,reuseaddr,fork", "EXEC:python3 /app/chall.py"]
