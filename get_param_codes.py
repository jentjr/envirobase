import numpy as np
import pandas as pd

def get_param_codes():
    url = "https://qwwebservices.usgs.gov/public_srsnames.xls"
    df = pd.read_excel(url, skiprows=6, dtype={0:np.dtype('U5')})
    return df

if __name__ == '__main__':
    df = get_param_codes()
    df.to_csv("param_codes.csv", encoding='utf-8', index=False, header=False)
