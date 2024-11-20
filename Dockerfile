FROM python:3.13

# Установка Google Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
RUN apt-get update -y
RUN apt-get install -y google-chrome-stable

COPY . .

RUN pip install -r requirements.txt

ENV DISPLAY=:99

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]