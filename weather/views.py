import requests
from django.shortcuts import render
from .models import City
from .forms import CityForm


def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=88b4fe5b5bb7aba71ff16b518ba97648'
    # city = 'Las Vegas'

    # saving city
    err_msg = ''
    message = ''
    message_class = ''
    if request.method == 'POST':
        form = CityForm(request.POST)

        # Prevent duplicate cities to be added
        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()

            if existing_city_count == 0:
                # checking if the city exists in an api
                r = requests.get(url.format(new_city)).json()
                # print(r)
                if r['cod'] == 200:
                    form.save()
                else:
                    err_msg = "City does not exist in the world!"
            else:
                err_msg = "City already exists in the list"


        if err_msg:
            message = err_msg
            message_class = 'is-danger'
        else:
            message = 'City added successfully!'
            message_class = 'is-success'


    # print(err_msg)
    form = CityForm()

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
    context = {
        'weather_data' : weather_data,
        'form': form,
        'message': message,
        'message_class': message_class
    }
    return render(request, 'weather/weather.html', context)
