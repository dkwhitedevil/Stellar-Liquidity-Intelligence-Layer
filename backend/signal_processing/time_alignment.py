import pandas as pd


def align_to_window(df, ts_col, window="5min"):
    df = df.copy()
    df["window"] = pd.to_datetime(df[ts_col]).dt.floor(window)
    return df
