import requests
from django.shortcuts import render
from .models import City


def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=88b4fe5b5bb7aba71ff16b518ba97648'
    city = 'Las Vegas'

    weather_data = []
    # db query
    cities = City.objects.all()
    for city in cities:

        r = requests.get(url.format(city)).json()
        # print(r.text)

        city_weather = {
            'city': city.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        }
        weather_data.append(city_weather)
    # print(weather_data)

    # print(city_weather)
    context = {'weather_data' : weather_data}
    return render(request, 'weather/weather.html', context)
