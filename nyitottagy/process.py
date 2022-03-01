import pandas as pd
from pathlib import Path
import scipy.spatial.distance
import numpy as np
import json


if __name__ == "__main__":

    def compacting(df, input_array):
        index = []
        for i in input_array:
            d = scipy.spatial.distance.cdist(list(df.values), i)
            index += ([d.T[i].argmin() for i in range(len(d.T))])
        return index

    data = pd.read_pickle("data.pkl")
    df = data.loc[:,["x_position","y_position","z_position"]]

    input_locations = json.loads(Path("input.json").read_text())
    #cut input into 4
    input = np.array([list(i.values()) for i in input_locations])
    if len(input_locations) == 5000:
        input = np.array_split(input, 10) #nézzük meg nyolccal is, és float64-ben
        indexes = compacting(df, input)
    else:
        d = scipy.spatial.distance.cdist(list(df.values), input) #nézzük meg nyolccal is, float64-ben

        indexes = [d.T[i].argmin() for i in range(len(d.T))]

    result = data.iloc[indexes, [0, -2, -1]].to_dict("records")
    Path("output.json").write_text(json.dumps(result))