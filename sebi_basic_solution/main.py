from pathlib import Path
import json
import pandas as pd
import numpy as np

pos_cols = [f"{ax}_position" for ax in ["x", "y", "z"]]


def get_distance(data_array: np.array, query_array: np.array):
    return np.square(data_array - query_array).sum()


def find_closest(data_array, query_array):
    return np.array(
        list(map(lambda vec: get_distance(vec, query_array), data_array))
    ).argmin()


if __name__ == "__main__":

    data = pd.read_parquet("data_subset.parquet")

    input_locations = json.loads(Path("input.json").read_text())
    input_array = map(lambda d: np.array(list(d.values())), input_locations)

    result_ids = list(
        map(
            lambda input_data: find_closest(
                data.loc[:, pos_cols].to_numpy(), input_data
            ),
            input_array,
        )
    )

    results = data.iloc[result_ids][["msec", "subject", "trial"]].to_dict("records")

    Path("output.json").write_text(json.dumps(results))
