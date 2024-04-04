import os
import json
from datetime import datetime
import holidays
import numpy as np


def load_json_data(filepath):
    with open(filepath, "r") as file:
        return json.load(file)


# Notizen : sleep data heart rates ,cleanen und gute Data suchen, danach Augmentation
# Kommentare nicht vergessen !!!
# Parser


def parse_sleep(data):
    records = []
    for entry in data:  # Scrolls through each day's data in the list
        # print("entry", entry)
        sleep_data = entry[
            "dailySleepDTO"
        ]  # Access to the daily sleep DTO for each entry
        # Calculation of sleep quality
        # (REM + deep sleep) / total sleep time * 100, minus percentage of waking state
        total_sleep_time = sleep_data["sleepTimeSeconds"] or 0
        rem_sleep_seconds = sleep_data["remSleepSeconds"] or 0
        deep_sleep_seconds = sleep_data["deepSleepSeconds"] or 0
        awake_sleep_seconds = sleep_data["awakeSleepSeconds"] or 0

        if total_sleep_time > 0:  # Prevents division by zero
            quality = (
                (rem_sleep_seconds + deep_sleep_seconds) / total_sleep_time * 100
            ) - (awake_sleep_seconds / total_sleep_time * 100)
        else:
            quality = 0  # Sets quality to 0 if no sleep time is specified

        sStart = 0
        sEnd = 0
        averageRespirationValue = 0
        lowestRespirationValue = 0
        highestRespirationValue = 0
        avgSleepStress = 0
        if sleep_data["sleepStartTimestampLocal"] != None:
            sStart = datetime.utcfromtimestamp(
                sleep_data["sleepStartTimestampLocal"] / 1000
            )
            sStart = sStart.hour * 60 + sStart.minute
        if sleep_data["sleepEndTimestampLocal"] != None:
            sEnd = datetime.utcfromtimestamp(
                sleep_data["sleepEndTimestampLocal"] / 1000
            )
            sEnd = sEnd.hour * 60 + sEnd.minute
        if "averageRespirationValue" in sleep_data.keys():
            averageRespirationValue = sleep_data["averageRespirationValue"]
        if "lowestRespirationValue" in sleep_data.keys():
            lowestRespirationValue = sleep_data["lowestRespirationValue"]
        if "highestRespirationValue" in sleep_data.keys():
            highestRespirationValue = sleep_data["highestRespirationValue"]
        if "avgSleepStress" in sleep_data.keys():
            avgSleepStress = sleep_data["avgSleepStress"]
        record = {
            "calendarDate": sleep_data["calendarDate"],
            "sleepTimeSeconds": sleep_data["sleepTimeSeconds"],
            "deepSleepSeconds": sleep_data["deepSleepSeconds"],
            "lightSleepSeconds": sleep_data["lightSleepSeconds"],
            "remSleepSeconds": sleep_data["remSleepSeconds"],
            "awakeSleepSeconds": sleep_data["awakeSleepSeconds"],
            "SleepStarthxm": sStart,
            "SleepEndhxm": sEnd,
            "sleepQuality": quality,  # Added attribute for sleep quality
            "avgRPV": averageRespirationValue,
            "minRPV": lowestRespirationValue,
            "maxRPV": highestRespirationValue,
            "avgSleepStress": avgSleepStress,
        }
        # print("record", record)
        records.append(record)
        # break

    return records


def parse_stress(data):
    # Erstellung eines Feiertagskalenders für Deutschland (bundesweit)
    de_holidays = holidays.CountryHoliday("DE")

    records = []
    for obj in data:
        # Umwandlung des Datums in ein datetime Objekt
        date_obj = datetime.strptime(obj["calendarDate"], "%Y-%m-%d")
        date_str = date_obj.strftime("%Y-%m-%d")

        # Prüfung, ob es sich um einen Dienstag (1) oder Mittwoch (2) handelt
        is_uni = (
            1 if date_obj.weekday() in [0, 1, 3] and date_str not in de_holidays else 0
        )
        stress_min = 0
        stress_max = 0
        stress_avg = 0
        bb_min = 0
        bb_max = 0
        bb_avg = 0
        vals = np.array(obj["stressValuesArray"])
        if len(vals.shape) == 2:
            stress_max = vals[:, 1].max()
            if stress_max > 0:
                stress_min = vals[:, 1][(vals[:, 1] > 0)].min()
                stress_avg = vals[:, 1][(vals[:, 1] > 0)].mean()
            vals = np.array(obj["bodyBatteryValuesArray"]).astype(str)
            val = vals[:, 2][(vals[:, 2] != "None")].astype(int)
            # if len(vals.shape) == 2:
            if len(val) >= 1:
                bb_max = val.max()
                if bb_max > 0:
                    bb_min = val[(val > 0)].min()
                    bb_avg = val[(val > 0)].mean()
        record = {
            "calendarDate": obj["calendarDate"],
            "maxStressLevel": obj["maxStressLevel"],
            "avgStressLevel": obj["avgStressLevel"],
            "minStressData": stress_min,
            "maxStressData": stress_max,
            "avgStressData": stress_avg,
            "minBBData": bb_min,
            "maxBBData": bb_max,
            "avgBBData": bb_avg,
            "is_uni": is_uni,  # Hinzugefügte Spalte für Dienstag/Mittwoch
        }
        records.append(record)
    return records


def parse_heart_rates(data):
    records = []
    for obj in data:
        # print("obj", obj)
        avg = 0
        hrr = np.array(obj["heartRateValues"])
        if len(hrr.shape) == 2:
            hr = hrr[:, 1]
            hr = hr[(hr != None)]
            avg = hr.mean()
            # print("obj", hr)
        records.append(
            {
                "calendarDate": obj["calendarDate"],
                "maxHeartRate": obj["maxHeartRate"],
                "minHeartRate": obj["minHeartRate"],
                "avgHeartRate": avg,
                "restingHeartRate": obj["restingHeartRate"],
                "lastSevenDaysAvgRestingHeartRate": obj[
                    "lastSevenDaysAvgRestingHeartRate"
                ],
            }
        )

    # print("record", records)

    return records


def parse_body_battery(data):
    classes = [None, "VERY_LOW", "LOW", "MODERATE", "HIGH"]
    records = []
    for day in data:
        for obj in day:
            record = {
                "date": obj["date"],
                "charged": obj["charged"],
                "drained": obj["drained"],
                # "startTimestampGMT": obj["startTimestampGMT"],
                # "endTimestampGMT": obj["endTimestampGMT"],
                # "startTimestampLocal": obj["startTimestampLocal"],
                # "endTimestampLocal": obj["endTimestampLocal"],
                "bodyBatteryDynamicFeedbackEvent": classes.index(
                    obj.get("bodyBatteryDynamicFeedbackEvent", {}).get(
                        "bodyBatteryLevel", None
                    )
                ),
                "endOfDayBodyBatteryLevel": classes.index(
                    obj.get("endOfDayBodyBatteryDynamicFeedbackEvent", {}).get(
                        "bodyBatteryLevel", None
                    )
                ),
            }
            records.append(record)

    return records


# Iter files


def insert_names(wn, name):
    for w in wn:
        w["names"] = name
    return wn


def iter_files(directory_path, with_names=False):
    stress_data = []
    heart_rates = []
    sleep_data = []
    body_battery = []

    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".json"):
                full_path = os.path.join(root, file)
                name = full_path.split("/")[-2]
                data = load_json_data(full_path)
                if "stress_data" in file:
                    if with_names:
                        stress_data.extend(insert_names(parse_stress(data), name))
                    else:
                        stress_data.extend(parse_stress(data))
                elif "heart_rates" in file:
                    if with_names:
                        heart_rates.extend(insert_names(parse_heart_rates(data), name))
                    else:
                        heart_rates.extend(parse_heart_rates(data))
                elif "sleep_data" in file:
                    if with_names:
                        sleep_data.extend(insert_names(parse_sleep(data), name))
                    else:
                        sleep_data.extend(parse_sleep(data))
                elif "body_battery" in file:
                    if with_names:
                        body_battery.extend(
                            insert_names(parse_body_battery(data), name)
                        )
                    else:
                        body_battery.extend(parse_body_battery(data))
                else:
                    print(f"Unrecognized file: {file}")
    return stress_data, heart_rates, sleep_data, body_battery


if __name__ == "__main__":
    import pandas as pd

    # filepath = "data/Liza/stress_data.json"
    # filepath = "data/Liza/body_battery.json"
    # filepath = "data/Liza/heart_rates.json"
    # filepath = "data/Liza/sleep_data.json"
    # print(os.getcwd())
    # data = load_json_data(filepath)
    filepath = "data"
    stress_data, heart_rates, sleep_data, body_battery = iter_files(filepath)
    df_stress_data = pd.DataFrame(stress_data)
    df_stress_data
    df_stress_data = df_stress_data.dropna()
    print(df_stress_data[(df_stress_data["minStressData"] != 0)])
