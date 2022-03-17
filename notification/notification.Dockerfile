FROM python:3-slim
WORKDIR /usr/src/app

COPY amqp.reqs.txt ./
RUN python -m pip install --no-cache-dir -r amqp.reqs.txt

COPY gmail.reqs.txt ./
RUN python -m pip install --no-cache-dir -r gmail.reqs.txt

COPY token.json ./
COPY amqp_send_email.py ./
COPY send_email.py ./
COPY amqp_setup.py ./
CMD [ "python", "./amqp_send_email.py" ]