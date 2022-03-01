import pandas as pd
import numpy as np
import json
import pickle
from pathlib import Path
import scipy.spatial.distance

pos_cols = [f"{ax}_position" for ax in ["x", "y", "z"]]

data = pd.read_parquet("data_subset.parquet")

input_locations = json.loads(Path("input.json").read_text())
input_locations = np.array(
    [tuple(pos.values()) for pos in input_locations], dtype=np.float64
)

n = len(input_locations)

if n > 10:
    with open("kdtree.pickle", "rb") as file:
        tree = pickle.load(file)

    dist, ind = tree.query(input_locations, k = 100, dualtree=True)

    results_index = [min([i for d, i in zip(d_vec, i_vec) if d == d_vec.min()]) for d_vec, i_vec in zip(dist, ind)]
    results = data.iloc[results_index, :][["msec", "subject", "trial"]].to_dict("records")
    Path("output.json").write_text(json.dumps(results))


else:

    if __name__ == "__main__":

        df = data.reset_index().loc[:,["x_position","y_position","z_position"]]

        input_locations = json.loads(Path("input.json").read_text())

        input = np.array([list(i.values()) for i in input_locations])

        d = scipy.spatial.distance.cdist(list(df.values), np.array(input))

        results_index = [d.T[i].argmin() for i in range(len(d.T))]

        result = data.iloc[results_index, [1, -2, -1]].to_dict("records")
        Path("output.json").write_text(json.dumps(result)) 






