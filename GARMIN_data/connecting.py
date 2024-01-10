from garmin_function import save_data
from garminconnect import (Garmin,  
                           GarminConnectConnectionError, 
                           GarminConnectAuthenticationError, 
                           GarminConnectTooManyRequestsError)
import datetime

def init_garmin_api(email, password):
    # Connect API
    try:  
        print("Try to connect with GARMIN...")
        api = Garmin(email, password)
        api.login() 
        print("Connected")
    # Error handling
    except(GarminConnectConnectionError, 
            GarminConnectAuthenticationError, 
            GarminConnectTooManyRequestsError
            ) as err: 
        return f"ERROR: {err}"
    return api

def logout_garmin_api(api):
    # Disonnect API -- if this wont happen the api will block further attempts
    api.login() 

if __name__ == "__main__":
    
    # Time span
    start_date = datetime.date(2023, 12, 7)
    end_date = datetime.date.today()

    # Link with Garmin-Connect account
    email = input("Email: ")
    password = input("Password: ")
    
    api = init_garmin_api(email, password)
    save_data(api, start_date, end_date)