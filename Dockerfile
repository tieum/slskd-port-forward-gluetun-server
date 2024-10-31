FROM python:3-alpine

WORKDIR /usr/src/app

RUN pip install --no-cache-dir kubernetes

COPY slskd.portfwd.py ./

CMD ["python", "./slskd.portfwd.py"]
