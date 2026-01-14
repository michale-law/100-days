import requests
import os
import time
import datetime as dt
from twilio.rest import Client
weather_endpoint = "https://api.openweathermap.org/data/2.5/forecast"
api_key = os.getenv("WEATHER_API_KEY")
twillo_recovery = os.getenv("Twilio_RECOVERY_CODE")
twillo_key = os.getenv("TWILLO_KEY")
Account_Sid = os.getenv("ACCOUNT_SID")
MESS_SERV_ID = os.getenv("MESS_SERV_ID")
TEST_NUM = os.getenv("TEST_NUM")
print("API key loaded:", api_key is not None)
print("Twillo key loaded:", twillo_key is not None)


params = {
    # Pick ONE approach: city query OR lat/lon.
    #"q": "Killeen,TX,US",
     "lat": 18.135660,
     "lon": -94.440224,
    "appid": api_key,
    "units": "imperial",
    'cnt':4,
}
response = requests.get(weather_endpoint, params=params)
response.raise_for_status()
weather_data=(response.json())
print(weather_data)
condition_list = []

for forcast in weather_data["list"]:
    conditon_id = forcast["weather"][0]["id"]
    condition_list.append(conditon_id)
print(condition_list)
def is_raining(condition_list):
    for condition in condition_list:
        if condition < 700:
            print("It will rain — send text")
            return True
    print("No rain in forecast window")
    return False
if is_raining(condition_list) == True:
    account_sid = Account_Sid
    auth_token = twillo_key
    client = Client(account_sid, auth_token)
try:
    message = client.messages.create(
      messaging_service_sid=MESS_SERV_ID,
      body='its gonna rain tomorrow ',
      to=TEST_NUM
    )
    print("Message SID:", message.sid)
    print("Message status:", message.status)
except Exception as e:
    print("Twilio error:", e)
is_raining(condition_list)