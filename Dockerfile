FROM python:3.9

# maintainer: Sebastian

WORKDIR /app

#RUN apt update && apt install -y unicorn

ADD requirements.txt . 

# install libs
RUN pip3 install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
# add app
COPY __init__.py .
COPY standAloneFastapi.py .
COPY supersecret.py .
# fastapi

CMD ["uvicorn", "standAloneFastapi:app", "--host", "0.0.0.0", "--port", "80"]

