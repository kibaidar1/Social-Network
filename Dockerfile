FROM python:3.12

RUN mkdir /social_network_api

WORKDIR /social_network_api

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

#CMD alembic upgrade head
#
#CMD gunicorn src.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
