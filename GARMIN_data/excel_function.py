import pandas as pd

def get_excel_data():
    df = pd.read_csv("./GARMIN_data/excel/stundenbuch.csv")
    df.columns = ["Zeitstempel","Mail","Start","Gefuehl Anfang", "Konzentration", "Gefuehl Ende", "Pausen", "Ende"]
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

if __name__ == "__main__":
    df = get_excel_data()
    print(df)
    # print(df.shape)