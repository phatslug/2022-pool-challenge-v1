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
    [tuple(pos.values()) for pos in input_locations], dtype=np.float32
)

n = input_locations.shape[0]

if n > 10:
    with open("kdtree.pickle", "rb") as file:
        tree = pickle.load(file)

    dist, ind = tree.query(input_locations, k = 100)

    results_index = [min([i for d, i in zip(d_vec, i_vec) if d == d_vec.min()]) for d_vec, i_vec in zip(dist, ind)]
    results = data.iloc[results_index, :][["msec", "subject", "trial"]].to_dict("records")
    Path("output.json").write_text(json.dumps(results))


else:

    d = scipy.spatial.distance.cdist(data.loc[:, pos_cols].values, input_locations)

    results_index = d.argmin(axis=0)

    result = data.loc[results_index, ["msec", "subject", "trial"]].to_dict("records")

    Path("output.json").write_text(json.dumps(result))