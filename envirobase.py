import numpy as np
import pandas as pd


def get_param_codes():
    url = "https://help.waterdata.usgs.gov/parameter_cd?group_cd=%"
    df = pd.read_html(url, header=0, converters={0: str})[0]
    df["Parameter Code"] = df.astype(np.dtype("U5"))
    df.to_csv("sql/data/param_codes.csv", encoding="utf-8", index=False, header=False)
    return df


def get_medium_codes():
    url = "https://help.waterdata.usgs.gov/medium_cd"
    df = pd.read_html(url, header=0, converters={0: str})[0]
    df.to_csv("sql/data/medium_codes.csv", encoding="utf-8", index=False, header=False)
    return df
