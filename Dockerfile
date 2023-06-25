# ChatGPTinTelegram Version: 2.0
FROM python:3
MAINTAINER Vit Valendovsky <valendovsky@gmail.com>
LABEL version='2.0'
WORKDIR /app
COPY requirements.txt ./
RUN pip3 install --upgrade setuptools
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .
CMD [ "python", "./main.py" ]