FROM python

# maintainer: Sebastian

RUN pip install -r requirements.txt

# fastapi
RUN uvicorn standAloneFastapi:app