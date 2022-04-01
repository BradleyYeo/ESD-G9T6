FROM python:3-slim
WORKDIR /usr/src/app
COPY cart.reqs.txt ./
RUN python -m pip install --no-cache-dir -r cart.reqs.txt
COPY ./cart.py .
CMD [ "python", "./cart.py" ]
