import requests
from django.shortcuts import render
from .models import City
from .forms import CityForm

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=f26b395d9f64f833516e9b1fadf08e29'
    city = 'Joinville'

    if request.method == 'POST':
        pass

    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    for city in cities:
        
        r = requests.get(url.format(city)).json()

        city_weather = {
            'city' : city.name,
            #'temperature' : r['main']['temp'],
            'temperature' : r.get('main').get('temp'),
            'description' : r.get('weather')[0].get('description'),
            'icon' :  r.get('weather')[0].get('icon'),
        }

        weather_data.append(city_weather)

    print(weather_data)

    context = {'weather_data' : weather_data, 'form' : form}

    return render(request, 'weather/weather.html', context)
