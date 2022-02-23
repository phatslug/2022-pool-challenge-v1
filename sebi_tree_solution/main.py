import pandas as pd
import numpy as np
import json
import pickle
from pathlib import Path

from sklearn.cluster import k_means

pos_cols = [f"{ax}_position" for ax in ["x", "y", "z"]]

if __name__ == "__main__":
    data = pd.read_parquet("data_subset.parquet")

    input_locations = json.loads(Path("input.json").read_text())
    input_locations = np.array([*map(lambda x: list(x.values()), input_locations)])

    with open("kdtree.pickle", "rb") as file:
        tree = pickle.load(file)

    dist, ind = tree.query(input_locations, k = 1000)

    results = data.iloc[[x[0] for x in ind], :][["msec", "subject", "trial"]].to_dict(
        "records"
    )
    Path("output.json").write_text(json.dumps(results))
