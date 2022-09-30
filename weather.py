import requests


API_KEY = "e62bec84225ae5e96ae63ee6c9d069aa"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"

def weather(city_name):
    complete_url = BASE_URL + "appid=" + API_KEY + "&q=" + city_name
    response = requests.get(complete_url)

    data = response.json()
    if data["cod"] != "404":
        y = data["main"]
        current_temperature = y["temp"]
        z = data["weather"]
        weather_description = z[0]["description"]

        return(" Temperature (in kelvin unit) = " +
                  str(current_temperature) + 
         "\n description = " +
                  str(weather_description))
    return "City Not Found"

city_name = input("Enter city name: ")
print(weather(city_name))
