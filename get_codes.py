import pandas as pd


def get_param_codes():
    url = "https://help.waterdata.usgs.gov/parameter_cd?group_cd=%"
    df = pd.read_html(url, header=0, converters={0: str})[0]
    df["Parameter Code"] = df.astype(np.dtype("U5"))
    df.to_csv("data/param_codes.csv", encoding="utf-8", index=False, header=False)
    return df


def get_medium_codes():
    url = "https://help.waterdata.usgs.gov/medium_cd"
    df = pd.read_html(url, header=0, converters={0: str})[0]
    df.to_csv("data/medium_codes.csv", encoding="utf-8", index=False, header=False)
    return df

if __name__ == '__main__':
    get_medium_codes()
    get_param_codes()
