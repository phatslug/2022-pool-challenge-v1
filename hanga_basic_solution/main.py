import json
import numpy as np
import pandas as pd

from pathlib import Path


axes = ["x", "y", "z"]
pos_cols = [f"{ax}_position" for ax in axes]


def get_closest_idx_for_point(data, point):
    return (data.loc[:, pos_cols] - point).pipe(np.square).sum(axis=1).idxmin()


if __name__ == "__main__":

    data = pd.read_parquet("filtered_data.parquet")
    input_locations = json.loads(Path("input.json").read_text())
    input_tuples = [tuple(d[pos_col] for pos_col in pos_cols)
                    for d in input_locations]
    fkeys = ["msec", "subject", "trial"]

    out = [
        data.loc[lambda df: get_closest_idx_for_point(
            df, point), fkeys].to_dict()
        for point in input_tuples
    ]
    Path("output.json").write_text(json.dumps(out))
