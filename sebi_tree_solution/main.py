import pandas as pd
import numpy as np
import json
import pickle
from pathlib import Path

pos_cols = [f"{ax}_position" for ax in ["x", "y", "z"]]

if __name__ == "__main__":
    data = pd.read_parquet("data_subset.parquet")

    input_locations = json.loads(Path("input.json").read_text())
    input_locations = np.array(
        [tuple(pos.values()) for pos in input_locations], dtype=np.float64
    )

    with open("kdtree.pickle", "rb") as file:
        tree = pickle.load(file)

    dist, ind = tree.query(input_locations, k = 10)

    results_index = [min([i for d, i in zip(d_vec, i_vec) if d == d_vec.min()]) for d_vec, i_vec in zip(dist, ind)]
    results = data.iloc[results_index, :][["msec", "subject", "trial"]].to_dict("records")
    Path("output.json").write_text(json.dumps(results))
