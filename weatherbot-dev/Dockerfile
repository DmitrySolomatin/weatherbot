# base image
FROM python:3.8-slim-buster
#ARG telegram_bot_token
ARG token
ARG api_key
ARG db_url
ENV APP_TOKEN=$token
ENV APP_WEATHER_KEY=$api_key
ENV APP_DATABASE_URL=&db_url

#docker build --build-arg token='yyyy' --build-arg api_key='yyyy' --build-arg db_url='yyyy' -t weather:v2 .

#example env and local var
# ARG telegram_bot_token
# ENV TELEGRAM_bot_token=$telegram_bot_token

RUN env | grep "APP_TOKEN"
RUN env | grep "APP_WEATHER_KEY"
RUN env | grep "APP_DATABASE_URL"
#workdir
WORKDIR /weatherbot-dev
RUN ./weatherbot-dev/createuser.sh
#upgrade pip
RUN pip install --upgrade pip
#install python modules needed by the app
COPY requirements.txt requirements.txt
#RUN python -m venv venv
#RUN venv/bin/pip install --no-cache-dir -r ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
#copy files required for the app run
COPY models.py weather.py weather_json.py ./weatherbot-dev/

#the port number the container should expose
EXPOSE 80
#run the application
CMD ["python", "weather.py"]
