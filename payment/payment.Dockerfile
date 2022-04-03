FROM python:3-slim
WORKDIR /usr/src/app

COPY payment.reqs.txt ./
RUN python -m pip install --no-cache-dir -r payment.reqs.txt

COPY payment.py ./
COPY .env ./
COPY stripe.exe .

# COPY templates . #this syntax doesn't work
# COPY ./templates/charge.html ./templates #REALIZED THAT NEED THE / AT THE END OR ELSE IT DOESN'T COPY OVER PROPERLY
# COPY ./templates/checkout.html ./templates #REALIZED THAT NEED THE / AT THE END OR ELSE IT DOESN'T COPY OVER PROPERLY
COPY ./templates/charge.html ./templates/
COPY ./templates/checkout.html ./templates/

# CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
CMD [ "python", "./payment.py" ]
