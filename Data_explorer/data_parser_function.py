import os
import json
from datetime import datetime
import holidays

def load_json_data(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)
    
# Parser

def parse_sleep(data):
    
    records = []
    for entry in data:  # Scrolls through each day's data in the list
        sleep_data = entry['dailySleepDTO']  # Access to the daily sleep DTO for each entry
        # Calculation of sleep quality
        # (REM + deep sleep) / total sleep time * 100, minus percentage of waking state
        total_sleep_time = sleep_data['sleepTimeSeconds'] or 0
        rem_sleep_seconds = sleep_data['remSleepSeconds'] or 0
        deep_sleep_seconds = sleep_data['deepSleepSeconds'] or 0
        awake_sleep_seconds = sleep_data['awakeSleepSeconds'] or 0
        
        if total_sleep_time > 0:  # Prevents division by zero
            quality = ((rem_sleep_seconds + deep_sleep_seconds) / total_sleep_time * 100) - (awake_sleep_seconds / total_sleep_time * 100)
        else:
            quality = 0  # Sets quality to 0 if no sleep time is specified
        record = {
            'calendarDate': sleep_data['calendarDate'],
            'sleepTimeSeconds': sleep_data['sleepTimeSeconds'],
            'deepSleepSeconds': sleep_data['deepSleepSeconds'],
            'lightSleepSeconds': sleep_data['lightSleepSeconds'],
            'remSleepSeconds': sleep_data['remSleepSeconds'],
            'awakeSleepSeconds': sleep_data['awakeSleepSeconds'],
            'sleepQuality': quality  # Added attribute for sleep quality
        }
        records.append(record)
    
    return records

def parse_stress(data):

    # Erstellung eines Feiertagskalenders für Deutschland (bundesweit)
    de_holidays = holidays.CountryHoliday('DE')

    records = []
    for obj in data:
        # Umwandlung des Datums in ein datetime Objekt
        date_obj = datetime.strptime(obj['calendarDate'], '%Y-%m-%d')
        date_str = date_obj.strftime('%Y-%m-%d')

        # Prüfung, ob es sich um einen Dienstag (1) oder Mittwoch (2) handelt
        is_tue_or_wed = 1 if date_obj.weekday() in [1, 2] and date_str not in de_holidays else 0

        record = {
            'calendarDate': obj['calendarDate'],
            'maxStressLevel': obj['maxStressLevel'],
            'avgStressLevel': obj['avgStressLevel'],
            'isTueOrWed': is_tue_or_wed  # Hinzugefügte Spalte für Dienstag/Mittwoch
        }
        records.append(record)

    return records

def parse_heart_rates(data):

    records = [
        {
            'calendarDate': obj['calendarDate'],
            'maxHeartRate': obj['maxHeartRate'],
            'minHeartRate': obj['minHeartRate'],
            'restingHeartRate': obj['restingHeartRate'],
            'lastSevenDaysAvgRestingHeartRate': obj['lastSevenDaysAvgRestingHeartRate']
        }
        for obj in data
    ]
        
    return records

def parse_body_battery(data):

    records = []
    for day in data:
        for obj in day:
            record = {
                'date': obj['date'],
                'charged': obj['charged'],
                'drained': obj['drained'],
                'startTimestampGMT': obj['startTimestampGMT'],
                'endTimestampGMT': obj['endTimestampGMT'],
                'startTimestampLocal': obj['startTimestampLocal'],
                'endTimestampLocal': obj['endTimestampLocal'],
                'endOfDayBodyBatteryLevel': obj.get('endOfDayBodyBatteryDynamicFeedbackEvent', {}).get('bodyBatteryLevel', None)
            }
            records.append(record)
    
    return records

# Iter files

def iter_files(directory_path):
    stress_data = []
    heart_rates = []
    sleep_data = []
    body_battery = []
    
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.json'):
                full_path = os.path.join(root, file)
                data = load_json_data(full_path)
                
                if 'stress_data' in file:
                    stress_data.extend(parse_stress(data))
                elif 'heart_rates' in file:
                    heart_rates.extend(parse_heart_rates(data))
                elif 'sleep_data' in file:
                    sleep_data.extend(parse_sleep(data))
                elif 'body_battery' in file:
                    body_battery.extend(parse_body_battery(data))
                else:
                    print(f"Unrecognized file: {file}")

    return stress_data, heart_rates, sleep_data, body_battery

if __name__ == "__main__":

    import pandas as pd

    filepath = 'data/Liza/stress_data.json'
    print(os.getcwd())
    data = load_json_data(filepath)
    print(type(data))
    df_stress_data = pd.DataFrame(parse_stress(data))
    print(df_stress_data)