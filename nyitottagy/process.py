import pandas as pd
from pathlib import Path
import scipy.spatial.distance
import numpy as np


if __name__ == "__main__":

    data = pd.read_pickle("data.pkl")
    df = data.reset_index().loc[:,["x_position","y_position","z_position"]]

    input_locations = json.loads(Path("input.json").read_text())

    input = np.array([list(i.values()) for i in input_locations])

    d = scipy.spatial.distance.cdist(list(df.values), np.array(input))

    shortest_index = [d.T[i].argmin() for i in range(len(d.T))]

    result = data.iloc[shortest_index, [1, -2, -1]].to_dict("records")
    Path("output.json").write_text(json.dumps(result))