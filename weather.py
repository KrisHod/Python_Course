import requests

city = 'Halifax'
url = 'http://api.weatherapi.com/v1/current.json?key=5cbbc609883b4758885203438230208&q='+city+'&aqi=no'
response = requests.get(url)
weather_json = response.json()

temp = weather_json.get('current').get('temp_c')
description = weather_json.get('current').get('condition').get('text')

print("Today's weather in", city, "is", description, "and", temp, "degrees")