FROM python:3.7-alpine
RUN pip install --upgrade pip
ADD ./python_code/* /code/
WORKDIR /code
#RUN apk add --no-cache --virtual .build-deps gcc g++
RUN pip install -r requirements.txt
CMD python3 kafka_2_elk_asamasach.py
