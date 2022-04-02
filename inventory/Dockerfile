FROM python:3.10-slim
WORKDIR /inventory
COPY inventory.reqs.txt inventory.reqs.txt
RUN python -m pip install --no-cache-dir -r inventory.reqs.txt
COPY . .

CMD [ "python", "./inventory.py"]
