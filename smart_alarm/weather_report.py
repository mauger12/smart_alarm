"""The weather_report function uses the open weather API to get
current weather information to be used in the __main__ module"""
import requests


def current_weather(city_name, units, api_key):
    """Takes a city, units and an API key and returns the current weather and temperature"""
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "q=" + city_name + "&units=" + units + "&appid=" + api_key
    response = requests.get(complete_url)
    weather_dict = response.json()

    main_data = weather_dict['main']
    current_temperature = str(round(main_data['temp']))

    weather_data = weather_dict['weather']
    weather_description = str(weather_data[0]['description'])
    report = str(" Today's weather is " + weather_description + " and a temperature of " +
                 current_temperature + " Celcius")
    return report
