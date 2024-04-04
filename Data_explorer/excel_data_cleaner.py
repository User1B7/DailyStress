import pandas as pd
import json
import warnings

warnings.simplefilter("ignore")


def get_excel_data(path_to_folder=""):
    new_url = path_to_folder+"data/stundenbuch.csv"
    df = pd.read_csv(new_url, sep=",", on_bad_lines="skip")
    df.columns = [
        "Time_stemp",
        "Mail",
        "Start",
        "Start_feeling",
        "Concentration",
        "End_feeling",
        "Brake",
        "End",
    ]

    df["Time_stemp"] = [d[0:10].replace("/", "-") for d in df["Time_stemp"]]
    df.fillna(0, inplace=True)
    df["Brake"] = [str(d).replace(" ", "").replace("bis", ",") for d in df["Brake"]]
    df["Pause Start"] = [str(d).split(",")[0] for d in df["Brake"]]
    df["Pause End"] = [str(d).split(",")[-1] for d in df["Brake"]]
    for i in range(len(df["Pause Start"])):
        if not ":" in str(df["Pause Start"][i]):
            df["Pause Start"][i] = 0
            df["Pause End"][i] = 0
    for i in range(len(df["Pause End"])):
        if not ":" in str(df["Pause End"][i]):
            df["Pause Start"][i] = 0
            df["Pause End"][i] = 0
    return df


def sort_by_names(path_to_folder="./"):
    df = get_excel_data(path_to_folder=path_to_folder)
    with open(f"{path_to_folder}data/names.json") as f:
        data = json.load(f)
    print(data)
    print(type(data))
    df["Name"] = ""
    for i in range(len(df["Mail"])):
        if df["Mail"][i] in data:
            df["Name"][i] = data[df["Mail"][i]]
    return df


if __name__ == "__main__":
    df = sort_by_names(path_to_folder="")
    print(df)
    # print(df.shape)
