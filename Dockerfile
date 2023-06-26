# ChatGPTinTelegram Version: 2.0
FROM python:3

MAINTAINER Vit Valendovsky <valendovsky@gmail.com>
LABEL version='2.0'

WORKDIR /app

ENV VIRTUAL_ENV=/env
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt ./
RUN pip3 install --upgrade setuptools
RUN pip3 install --no-cache-dir -r requirements.txt
RUN apt-get -y update
RUN apt-get install ffmpeg libsm6 libxext6  -y

COPY . .

CMD [ "python", "./main.py" ]