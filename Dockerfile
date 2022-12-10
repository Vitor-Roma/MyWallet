FROM python:3.8.4
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
WORKDIR /usr/src/app
COPY ./ /usr/src/app
RUN apt-get clean && apt-get update
RUN apt-get install -y gcc python3-dev python-dev build-essential default-libmysqlclient-dev musl-dev python-mysqldb
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
