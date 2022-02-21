from pathlib import Path
import json
import pandas as pd
import numpy as np
import numba

pos_cols = [f"{ax}_position" for ax in ["x", "y", "z"]]


@numba.jit(nopython=True, nogil=True, parallel=True)
def get_distance(data_pos: np.array, query_pos: np.array):
    return np.square(data_pos - query_pos).sum()


@numba.jit(nopython=True, nogil=True, parallel=True)
def find_closest(data_array: np.array, query_pos: np.array):
    distance_vec = []
    for data_pos in data_array:
        distance_vec.append(get_distance(data_pos, query_pos))
    return np.array(distance_vec).argmin()


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
