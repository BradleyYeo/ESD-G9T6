FROM python:3-slim
WORKDIR /usr/src/app
COPY http.reqs.txt ./
RUN python -m pip install --no-cache-dir -r http.reqs.txt

COPY amqp.reqs.txt ./
RUN python -m pip install --no-cache-dir -r amqp.reqs.txt

COPY ./order_history_wrapper.py ./invokes.py ./
COPY  ./amqp_setup.py ./

CMD [ "python", "./order_history_wrapper.py" ]