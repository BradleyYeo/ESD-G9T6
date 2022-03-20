FROM python:3-slim
WORKDIR /usr/src/app

COPY inventory.reqs.txt /
RUN pip install -r /inventory.reqs.txt
COPY . /app
WORKDIR /app
EXPOSE 5023
CMD ["python" , "./inventory.py"]
