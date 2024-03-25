import pandas as pd
import json
import warnings

warnings.simplefilter("ignore")


def get_excel_data():
    url2 = "https://docs.google.com/spreadsheets/d/1-5QijnBttDqLJFZssCqQ4vqi7CBir6LY4ctp8qOqwQw/edit#gid=1351272459"
    url_part1 = "/".join(url2.split("/")[:-1])
    url_part2 = url2.split("/")[-1][-10:]
    new_url = f"{url_part1}/export?gid={url_part2}&format=csv"
    df = pd.read_csv(new_url, sep=",", on_bad_lines="skip")
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
    print(df.head())
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


def sort_by_names():
    df = get_excel_data()
    with open("./data/names.json") as f:
        data = json.load(f)
    print(data)
    print(type(data))
    df["Name"] = ""
    for i in range(len(df["Mail"])):
        if df["Mail"][i] in data:
            df["Name"][i] = data[df["Mail"][i]]
    return df


if __name__ == "__main__":
    df = sort_by_names()
    print(df)
    # print(df.shape)
