import requests
import json
import os
import math
from datetime import datetime, timedelta

from dotenv import load_dotenv

load_dotenv()
<<<<<<< HEAD
<<<<<<< HEAD
API_KEY = os.getenv('APP_WEATHER_KEY')


def get_weather(loc):
    try:
        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}'.format(loc, API_KEY)
        data = requests.get(url)
        response = json.loads(data.content.decode('utf8'))
        city = response['name']
        country = response['sys']['country']
        temp = math.ceil(response['main']['temp'])
        feels_like = math.ceil(response['main']['feels_like'])
        main = [i['description'] for i in response['weather']]
        day = datetime.today().strftime('%a (%m-%d)')
        msg = '{}. Daily weather forecast in {}, {}: {}°C, feels like {}°C, {}.'.format(day, city, country, temp,
                                                                                        feels_like, "".join(main))
    except:
        pass

=======
=======
>>>>>>> 460c441d36fe8523fee39d3094e219a19444f074
API_KEY= os.getenv('APP_WEATHER_KEY')


def get_weather(loc):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}'.format(loc, API_KEY)
    data = requests.get(url)
    response = json.loads(data.content.decode('utf8'))
    city = response['name']
    country = response['sys']['country']
    temp = math.ceil(response['main']['temp'])
    feels_like = math.ceil(response['main']['feels_like'])
    main = [i['description'] for i in response['weather']]
    day = datetime.today().strftime('%a (%m-%d)')
    msg = '{}. Daily weather forecast in {}, {}: {}°C, feels like {}°C, {}.'.format(day, city, country, temp,
                                                                                    feels_like, "".join(main))
>>>>>>> 460c441d36fe8523fee39d3094e219a19444f074
    return msg


def geo_weather(lon, lat):
    url = 'http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&units=metric&appid={}'.format(lat, lon, API_KEY)
    data = requests.get(url)
    response = json.loads(data.content.decode('utf8'))
    city = response['name']
    country = response['sys']['country']
    temp = math.ceil(response['main']['temp'])
    feels_like = math.ceil(response['main']['feels_like'])
    main = [i['description'] for i in response['weather']]
    day = datetime.today().strftime('%a (%m-%d)')
    msg = '{}. Daily weather forecast in {}, {}: {}°C, feels like {}°C, {}.'.format(day, city, country, temp,
                                                                                    feels_like, "".join(main))
    return msg


def get_weather_5(loc):
<<<<<<< HEAD
<<<<<<< HEAD
    try:
        url = 'http://api.openweathermap.org/data/2.5/forecast?q={}&units=metric&cnt=5&appid={}'.format(loc, API_KEY)
        data = requests.get(url)
        response = json.loads(data.content.decode('utf8'))
        # json request has {keys:values} pairs, data separation
        cityn = response['city']['name']
        country = response['city']['country']
        datalist = response['list']
        count = 0  # day count
        day = []  # for day list
        msg = []  # for message list
        # data as a nested dictionary, getting their
        for i in range(0, len(datalist)):
            temp = [math.ceil(i['main']['temp']) for i in datalist]
            feels_like = [math.ceil(i['main']['feels_like']) for i in datalist]
            main = [i['weather'] for i in response['list']]
            spec = [item['description'] for sublist in main for item in sublist]
            count += i
            day.append((datetime.today() + timedelta(days=count)).strftime('%a (%m-%d)'))
            msg.append(day[i] + ": " + str(temp[i]) + "°C, feels like " + str(feels_like[i]) + "°C, " + str(spec[i]))
        msgg = '{},{}. 5 Day Weather Forecast: '.format(cityn, country)
    except:
        pass

=======
=======
>>>>>>> 460c441d36fe8523fee39d3094e219a19444f074
    url = 'http://api.openweathermap.org/data/2.5/forecast?q={}&units=metric&cnt=5&appid={}'.format(loc, API_KEY)
    data = requests.get(url)
    response = json.loads(data.content.decode('utf8'))
    # json request has {keys:values} pairs, data separation
    cityn = response['city']['name']
    country = response['city']['country']
    datalist = response['list']
    count = 0  # day count
    day = []  # for day list
    msg = []  # for message list
    # data as a nested dictionary, getting their
    for i in range(0, len(datalist)):
        temp = [math.ceil(i['main']['temp']) for i in datalist]
        feels_like = [math.ceil(i['main']['feels_like']) for i in datalist]
        main = [i['weather'] for i in response['list']]
        spec = [item['description'] for sublist in main for item in sublist]
        count += i
        day.append((datetime.today() + timedelta(days=count)).strftime('%a (%m-%d)'))
        msg.append(day[i] + ": " + str(temp[i]) + "°C, feels like " + str(feels_like[i]) + "°C, " + str(spec[i]))
    msgg = '{},{}. 5 Day Weather Forecast: '.format(cityn, country)
>>>>>>> 460c441d36fe8523fee39d3094e219a19444f074
    return msgg + "\n" + "\n".join([msg[i] for i in range(0, len(msg))])


def geo_weather_5(lon, lat):
    url = 'http://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&units=metric&cnt=5&appid={}'.format(lat, lon,
                                                                                                             API_KEY)
    data = requests.get(url)
    response = json.loads(data.content.decode('utf8'))
    # json request has {keys:values} pairs, data separation
    city = response['city']['name']
    country = response['city']['country']
    datalist = response['list']
    count = 0  # day count
    day = []  # for day list
    msg = []  # for message list
    # data as a nested dictionary, getting their
    for i in range(0, len(datalist)):
        temp = [math.ceil(i['main']['temp']) for i in datalist]
        feels_like = [math.ceil(i['main']['feels_like']) for i in datalist]
        main = [i['weather'] for i in response['list']]
        spec = [item['description'] for sublist in main for item in sublist]
        count += i
        day.append((datetime.today() + timedelta(days=count)).strftime('%a (%m-%d)'))
        msg.append(day[i] + ": " + str(temp[i]) + "°C, feels like " + str(feels_like[i]) + "°C, " + str(spec[i]))
    msgg = '{},{}. 5 Day Weather Forecast: '.format(city, country)
    return msgg + "\n" + "\n".join([msg[i] for i in range(0, len(msg))])
