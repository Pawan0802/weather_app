import requests
from django.shortcuts import render


def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=88b4fe5b5bb7aba71ff16b518ba97648'
    city = 'Las Vegas'

    r = requests.get(url.format(city)).json()
    # print(r.text)

    city_weather = {
        'city': city,
        'temperature': r['main']['temp'],
        'description': r['weather'][0]['description'],
        'icon': r['weather'][0]['icon'],
    }

    # print(city_weather)
    context = {'city_weather' : city_weather}
    return render(request, 'weather/weather.html', context)
