import pandas as pd
import json


def get_excel_data():
    df = pd.read_csv("./GARMIN_data/excel/stundenbuch.csv")
    df.columns = [
        "Zeitstempel",
        "Mail",
        "Start",
        "Gefuehl Anfang",
        "Konzentration",
        "Gefuehl Ende",
        "Pausen",
        "Ende",
    ]
    df["Zeitstempel"] = [d[0:10] for d in df["Zeitstempel"]]
    df.fillna(0, inplace=True)
    df["Pausen"] = [str(d).replace(" ", "").replace("bis", ",") for d in df["Pausen"]]
    df["Pause Start"] = [str(d).split(",")[0] for d in df["Pausen"]]
    df["Pause Ende"] = [str(d).split(",")[-1] for d in df["Pausen"]]
    for i in range(len(df["Pause Start"])):
        if not ":" in str(df["Pause Start"][i]):
            df["Pause Start"][i] = 0
            df["Pause Ende"][i] = 0
    for i in range(len(df["Pause Ende"])):
        if not ":" in str(df["Pause Ende"][i]):
            df["Pause Start"][i] = 0
            df["Pause Ende"][i] = 0
    return df


def get_json_name_data():
    with open("./GARMIN_data/json/names.json") as f:
        data = json.load(f)

    # Convert JSON to Pandas DataFrame
    df = pd.DataFrame(data)
    return df


def sort_by_names():
    df = get_excel_data()
    with open("./GARMIN_data/json/names.json") as f:
        data = json.load(f)
    print(data)
    print(type(data))
    # df2 = get_json_name_data()
    df["Name"] = ""
    for i in range(len(df["Mail"])):
        if df["Mail"][i] in data:
            df["Name"][i] = data[df["Mail"][i]]
    return df


if __name__ == "__main__":
    df = sort_by_names()
    print(df)
    # print(df.shape)
