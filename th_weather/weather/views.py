
from django.shortcuts import redirect, render
import requests

from .forms import CityForm
from .models import City

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=a4a79e2a0b10c8737936e036e82e348c'
    if request.method == 'POST': 
        form = CityForm(request.POST) 
        form.save() 
    form = CityForm()
    city = 'Las Vegas'
    cities = City.objects.all() 

    weather_data = []

    for city in cities:

        city_weather = requests.get(url.format(city)).json() 

        weather = {
            'city' : city,
            'temperature' : city_weather['main']['temp'],
            'description' : city_weather['weather'][0]['description'],
            'icon' : city_weather['weather'][0]['icon']
        }

        weather_data.append(weather) 

    context = {'weather_data' : weather_data, 'form' : form}

    return render(request, 'weather/index.html', context)


    
def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    return redirect('index')