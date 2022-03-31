FROM python:3.8-slim-buster
WORKDIR /usr/src/app

COPY inventory.reqs.txt ./
RUN python -m pip install --no-cache-dir -r inventory.reqs.txt
COPY inventory.py .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
