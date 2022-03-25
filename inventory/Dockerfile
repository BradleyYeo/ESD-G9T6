FROM python:3-slim
WORKDIR /usr/src/app

COPY inventory.reqs.txt ./
RUN python -m pip install --no-cache-dir -r inventory.reqs.txt
COPY ../inventory/inventory.py .

CMD ["python" , "./inventory.py"]
