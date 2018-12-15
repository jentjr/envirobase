import numpy as np
import pandas as pd


def get_param_codes():
    url = "https://help.waterdata.usgs.gov/parameter_cd?group_cd=%"
    df = pd.read_html(url, header=0, converters={0: str})[0]
    df["Parameter Code"] = df.astype(np.dtype("U5"))
    return df


if __name__ == "__main__":
    df = get_param_codes()
    df.to_csv("data/param_codes.csv", encoding="utf-8", index=False, header=False)
