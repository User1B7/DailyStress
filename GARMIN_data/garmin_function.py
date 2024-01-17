import datetime, os, json
from tqdm import tqdm

def get_steps_data(api, start_date):
    try:
        steps_data = api.get_steps_data(start_date)
    except Exception as e:
        return f"An error has occurred: {e}"
    return steps_data

def get_heart_rates(api, start_date):
    try:
        steps_data = api.get_heart_rates(start_date)
    except Exception as e:
        return f"An error has occurred: {e}"
    return steps_data

def get_sleep_data(api, start_date):
    try:
        steps_data = api.get_sleep_data(start_date)
    except Exception as e:
        return f"An error has occurred: {e}"
    return steps_data

def get_stress_data(api, start_date):
    try:
        steps_data = api.get_stress_data(start_date)
    except Exception as e:
        return f"An error has occurred: {e}"
    return steps_data

def get_body_battery(api, start_date):
    try:
        steps_data = api.get_body_battery(start_date)
    except Exception as e:
        return f"An error has occurred: {e}"
    return steps_data

def get_rhr_day(api, start_date):
    try:
        steps_data = api.get_rhr_day(start_date)
    except Exception as e:
        return f"An error has occurred: {e}"
    return steps_data

def get_blood_pressure(api, start_date):
    try:
        steps_data = api.get_blood_pressure(start_date)
    except Exception as e:
        return f"An error has occurred: {e}"
    return steps_data

def get_respiration_data(api, start_date):
    try:
        steps_data = api.get_respiration_data(start_date)
    except Exception as e:
        return f"An error has occurred: {e}"
    return steps_data

def log_data(api, start_date, end_date, func):
    logged_data = []
    # Calculate the number of days for the progress bar
    total_days = (end_date - start_date).days + 1
    
    # Iterate from start to end date through the data with tqdm progressbar
    with tqdm(total=total_days, desc=func.__name__) as pbar:
        for date in (start_date + datetime.timedelta(n) for n in range(
            (end_date - start_date).days + 1)):
            
            device_activity = func(api, date)
            # Add the data to a total list
            logged_data.append(device_activity)
            pbar.update(1)

        return logged_data

def save_data(api, start_date, end_date, 
             func=[get_heart_rates, get_sleep_data, 
                   get_stress_data, get_body_battery]):
    directory_path = "data/"
    # Check for path
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    # Create csv or json for every function in list
    for i, f in enumerate(func, start=1):
        file_path = os.path.join(directory_path, f.__name__[4:] + ".json")
        print(f"{i}/{len(func)} - Retrieving {f.__name__[4:]}")
        data = log_data(api, start_date, end_date, f)
        
        if data is not None:
            with open(file_path, "w") as json_file:
                json.dump(data, json_file) 

if __name__ == "__main__":
    from connecting import init_garmin_api
    
    start_date = datetime.date(2023, 12, 7)
    end_date = datetime.date.today()

    # Enter your email address and password here to test individual methods more quickly with the api
    email = "big0brudi@gmail.com"
    password = "IDontKnow1"
    
    api = init_garmin_api(email, password)

    save_data(api, start_date, end_date, func=[get_steps_data, get_heart_rates, get_sleep_data, 
                   get_stress_data, get_body_battery, get_rhr_day, 
                   get_blood_pressure, get_respiration_data])
    api.logout()