import pandas as pd
import random
from tqdm import tqdm


# create augmentation for pandas dataframes
# n defines how many new rows should be inserted
# distance defines how far the range is of allowed new values to the original value in percentage
# not_changeable defines the columns, which shouldnt be changed, those will just get copied
def augmentation(
    df,
    n=100,
    distance=0.05,
    not_changeable=[
        "bodyBatteryDynamicFeedbackEvent",
        "endOfDayBodyBatteryLevel",
        "is_uni",
    ],
):
    # Lables and classifiers must be implemented in here to not change their values

    not_ch_index = [list(df.columns).index(nch) for nch in not_changeable]
    new_df = df.astype(float)
    rows_l = []
    for index, row in tqdm(df.iterrows(), total=df.shape[0]):
        for i in range(n):
            col_l = []
            for j, col in enumerate(row):
                if j in not_ch_index:
                    col_l.append(col)
                else:
                    col_l.append(
                        random.uniform(col - (col * distance), col + (col * distance))
                    )
            rows_l.append(col_l)
    rows_df = pd.DataFrame(rows_l, columns=list(df.columns))
    new_df = pd.concat([new_df, rows_df], axis=0)
    return new_df


if __name__ == "__main__":
    import os
    import data_parser_function as dp

    current_dir = os.getcwd()
    stress_data, heart_rates, sleep_data, body_battery = dp.iter_files(
        os.path.join(current_dir, "data")
    )

    # create DataFrames
    df_stress_data = pd.DataFrame(stress_data)
    df_heart_rates = pd.DataFrame(heart_rates)
    df_sleep_data = pd.DataFrame(sleep_data)
    df_body_battery = pd.DataFrame(body_battery)

    df_merged = df_body_battery.merge(
        df_heart_rates, left_on="date", right_on="calendarDate", how="outer"
    )
    df_merged = df_merged.merge(df_stress_data, on="calendarDate", how="outer")
    df_merged = df_merged.merge(df_sleep_data, on="calendarDate", how="outer")
    df_merged = df_merged.dropna(axis=0)
    features = df_merged.drop(columns=["date", "calendarDate"])
    print(features.shape)
    ag = augmentation(features)
    print(ag.shape)
