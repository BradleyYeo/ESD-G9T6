FROM python:3-slim
WORKDIR /usr/src/app
COPY order_history_requirements.txt ./
RUN python -m pip install --no-cache-dir -r order_history_requirements.txt
COPY ./order_history.py .
CMD [ "python", "./order_history.py" ]
