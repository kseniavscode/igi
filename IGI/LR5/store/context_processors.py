import requests
import datetime
import calendar
from django.utils import timezone

from django.conf import settings

def header_data(request):

    api_key = settings.WEATHER_KEY
    city = 'Minsk'
    weather_data = {}

    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        res = requests.get(url, timeout=1).json()
        weather_data = {
            'temp': round(res['main']['temp']),
            'desc': res['weather'][0]['description'],
        }
    except:
        pass

    now = datetime.datetime.now()
    cal = calendar.TextCalendar(calendar.MONDAY)
    text_calendar = cal.formatmonth(now.year, now.month)

    utc_now = timezone.now() 
    local_now = timezone.localtime(utc_now)

    return {
        'header_weather': weather_data,
        'header_calendar': text_calendar,
        'utc_time': utc_now,
        'local_time': local_now,
        'city_name': city
    }