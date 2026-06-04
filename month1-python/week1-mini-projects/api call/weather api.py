import requests
import os
import json
from datetime import datetime

FILENAME = "datahis.json"

def get_api(option):
    full_data = []

    while True:
        try:
            no = int(input("for how many places you want weather update? : "))
            if no <= 0:
                print("number must be greater than 0")
                continue
            else:
                break
        except ValueError:
            print("you must enter only numbers")
            continue
 
    cities = []
    for i in range(0, no):
        city = input("enter the place name : ").strip()
        cities.append(city)

    api_key = "59fae7c1ec69554d4f719afbc006492d"

    if option == 1:
        for i in cities:
            try:
                request = requests.get(
                    f"https://api.openweathermap.org/data/2.5/weather?q={i}&appid={api_key}&units=metric"
                )
                if request.status_code == 200:
                    print(f"✅ connection established for {i}")
                    data = request.json()
                    full_data.append(data)
                elif request.status_code == 404:
                    print(f"❌ city '{i}' not found — check spelling")
                elif request.status_code == 401:
                    print("❌ invalid api key")
                else:
                    print(f"❌ api request failed for {i} — status {request.status_code}")
            except requests.exceptions.ConnectionError:
                print("❌ no internet connection")

    elif option == 2:
        for i in cities:
            try:
                request = requests.get(
                    f"https://api.openweathermap.org/data/2.5/forecast?q={i}&appid={api_key}&units=metric"
                )
                if request.status_code == 200:
                    print(f"✅ connection established for {i}")
                    data = request.json()
                    full_data.append(data)
                elif request.status_code == 404:
                    print(f"❌ city '{i}' not found — check spelling")
                elif request.status_code == 401:
                    print("❌ invalid api key")
                else:
                    print(f"❌ api request failed for {i} — status {request.status_code}")
            except requests.exceptions.ConnectionError:
                print("❌ no internet connection")

    return full_data

def store_data(full_data, option):
    datahistory = []

    if option == 1:
        for data in full_data:
            temperature  = data['main']['temp']
            feels_like   = data['main']['feels_like']
            pressure     = data['main']['pressure']
            humidity     = data['main']['humidity']
            visibility   = data['visibility']
            wind_speed   = data['wind']['speed']
            condition    = data['weather'][0]['description'].capitalize()
            place        = data['name']
            country      = data['sys']['country']
            temp_f       = round(temperature * 9/5 + 32, 1)

            datahis = {
                "LOCATION"    : place,
                "COUNTRY"     : country,
                "TEMPERATURE" : f"{temperature}°C / {temp_f}°F",
                "FEELS LIKE"  : f"{feels_like}°C",
                "CONDITION"   : condition,
                "PRESSURE"    : pressure,
                "HUMIDITY"    : humidity,
                "VISIBILITY"  : visibility,
                "WIND SPEED"  : wind_speed,
                "SEARCHED AT" : datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            datahistory.append(datahis)

    elif option == 2:
        for data in full_data:
            place   = data['city']['name']
            country = data['city']['country']
            seen_dates = []
            forecasts  = []
            for entry in data['list']:
                date = entry['dt_txt'].split(" ")[0]  
                if date not in seen_dates:
                    seen_dates.append(date)
                    forecasts.append({
                        "DATE"      : date,
                        "TEMP"      : f"{entry['main']['temp']}°C",
                        "CONDITION" : entry['weather'][0]['description'].capitalize(),
                        "HUMIDITY"  : entry['main']['humidity']
                    })
            datahis = {
                "LOCATION"  : place,
                "COUNTRY"   : country,
                "FORECAST"  : forecasts,
                "SEARCHED AT": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            datahistory.append(datahis)

    return datahistory

def save_data(datahistory):
    existing = []
    if os.path.exists(FILENAME):
        with open(FILENAME, "r") as file:
            try:
                existing = json.load(file)
            except json.JSONDecodeError:
                existing = []
    existing.extend(datahistory)
    with open(FILENAME, "w") as file:
        json.dump(existing, file, indent=4)
    print("✅ data saved to history")

def display_data(datahistory, option):
    if not datahistory:
        print("❌ no data to display")
        return

    if option == 1:
        for i in datahistory:
            print("\n" + "=" * 45)
            print(f"📍 {i['LOCATION']}, {i['COUNTRY']}")
            print(f"🌡️  Temperature  : {i['TEMPERATURE']}")
            print(f"🌡️  Feels Like   : {i['FEELS LIKE']}")
            print(f"☁️  Condition    : {i['CONDITION']}")
            print(f"💧 Humidity      : {i['HUMIDITY']}%")
            print(f"🔵 Pressure      : {i['PRESSURE']} hPa")
            print(f"👁️  Visibility   : {i['VISIBILITY']} m")
            print(f"🌬️  Wind Speed   : {i['WIND SPEED']} km/h")
            print("=" * 45)

        if len(datahistory) > 1:
            print("\n" + "=" * 55)
            print(f"{'CITY':<20} {'TEMP':>10} {'HUMIDITY':>10}")
            print("=" * 55)
            for i in datahistory:
                print(f"{i['LOCATION']:<20} {i['TEMPERATURE']:>10} {i['HUMIDITY']:>9}%")
            print("=" * 55)

    elif option == 2:
        for i in datahistory:
            print("\n" + "=" * 45)
            print(f"📍 {i['LOCATION']}, {i['COUNTRY']} — 5 Day Forecast")
            print("=" * 45)
            for day in i['FORECAST']:
                print(f"📅 {day['DATE']}  🌡️  {day['TEMP']}  ☁️  {day['CONDITION']}  💧{day['HUMIDITY']}%")
            print("=" * 45)

def view_data_history():
    if not os.path.exists(FILENAME):
        print("📭 no search history yet")
        return
    with open(FILENAME, "r") as file:
        try:
            history = json.load(file)
        except json.JSONDecodeError:
            print("❌ history file is corrupted")
            return
    if not history:
        print("📭 no search history yet")
        return
    print("\n" + "=" * 45)
    print("         🕒 SEARCH HISTORY")
    print("=" * 45)
    for entry in history:
        print(f"📍 {entry.get('LOCATION', '?')}, {entry.get('COUNTRY', '?')}")
        print(f"   🕒 {entry.get('SEARCHED AT', '?')}")
        print("-" * 45)

def main():
    while True:
        print("\n" + "=" * 45)
        print("          🌤️  WEATHER APP")
        print("=" * 45)
        print("1 - today's weather")
        print("2 - 5 day forecast")
        print("3 - view search history")
        print("4 - exit")

        while True:
            try:
                option = int(input("enter option number from above options: ")) 
                if option in range(1, 5):
                    break
                else:
                    print("you must enter only numbers from [1-4]")
            except ValueError:
                print("you must only type numbers in range [1-4]")

        if option == 3:
            view_data_history()
        elif option == 4:
            print("👋 bye!")
            break
        else:
            full_data = get_api(option)
            if full_data:
                datahistory = store_data(full_data, option)
                display_data(datahistory, option)
                save_data(datahistory)

if __name__ == "__main__":
    main()