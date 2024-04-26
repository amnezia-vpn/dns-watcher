FROM python:3.11-slim-bookworm

WORKDIR /app 

COPY main.py requirements.txt /app

RUN pip3 install -r requirements.txt --no-cache-dir

ENTRYPOINT ["python3", "main.py"]
