import json
#import logging
import os
from datetime import date, timedelta
#from garth.exc import GarthHTTPError

from garminconnect import (
    Garmin,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
    GarminConnectAuthenticationError,
)
from getpass import getpass


#logging.basicConfig(level=logging.INFO)
#logger = logging.getLogger(__name__)


def getDays():
    today = date.today()
    yesterday = today - timedelta(days=1)
    yesterday = yesterday.isoformat()
    return yesterday, today

# Load environment variables if defined
#email = os.getenv("EMAIL")
#password = os.getenv("PASSWORD")
#tokenstore = os.getenv("GARMINTOKENS") or "~/.garminconnect"
api = None

email = "your@mail.com"
password = "Password"

garmin = Garmin(email, password)
#garmin.logout()

print(garmin)
garmin.login()

print(garmin.display_name)

#%%

GARTH_HOME = os.getenv("GARTH_HOME", "~/.garth")
garmin.garth.dump(GARTH_HOME)

yesterday, today = getDays()
#print(garmin.get_stats(yesterday).keys())
#print(garmin.get_steps_data(yesterday)[:2])
#print(garmin.get_body_battery(yesterday)[0])
#print(garmin.get_blood_pressure(yesterday))
#print(garmin.get_spo2_data(yesterday))
#print(garmin.get_stress_data(yesterday))
#print(garmin.get_activity_details(0))

#%%

garmin.logout()

