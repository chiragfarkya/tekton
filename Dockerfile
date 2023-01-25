FROM python:3.8.10

RUN apt-get clean \
    && apt-get -y update

RUN apt-get -y install \
    python3-dev \
    build-essential

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt --src /usr/local/src

COPY templates /app/templates
COPY main.py /app/main.py

EXPOSE 5000
CMD [ "python", "main.py" ]
