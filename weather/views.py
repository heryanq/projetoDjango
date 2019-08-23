import requests
from django.shortcuts import render, redirect
from .models import City
from .forms import CityForm

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=f26b395d9f64f833516e9b1fadf08e29'

    err_msg = ''
    message = ''
    message_class = ''

    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()

            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()

                if r['cod'] == 200:
                    form.save()
                else:
                    err_msg = 'This city is invalid'

            else:
                err_msg = 'City already exists in the list!'

        if err_msg:
            message = err_msg
            message_class = 'is-danger'
        else:
            message = 'City added sucessfully'
            message_class = 'is-success'

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

    context = {
            'weather_data' : weather_data,
            'form' : form,
            'message' : message,
            'message_class' : message_class
    }

    return render(request, 'weather/weather.html', context)

def about(request):
    return render(request, 'weather/about.html')

def contact(request):
    return render(request, 'weather/contact.html')


def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()

    return redirect('index')
