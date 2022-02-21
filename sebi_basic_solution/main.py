from pathlib import Path
import json
import pandas as pd
import numpy as np


def get_square_distance(data_array: np.array, query_array: np.array):
    return ((data_array - query_array) ** 2).sum()


def find_closest(data_array: np.array, query_array: np.array):
    return np.array(
        list(map(lambda vec: get_square_distance(vec, query_array), positions))
    ).argmin()


if __name__ == "__main__":
    data = pd.read_csv("data.csv")[lambda _df: _df["entity_id"] == 0]
    input_locations = json.loads(Path("input.json").read_text())
    input_locations = map(lambda d: np.array(list(d.values())), input_locations)

    positions = data.loc[:, [f"{ax}_position" for ax in ["x", "y", "z"]]].to_numpy()

    result_ids = list(
        map(lambda input_data: find_closest(positions, input_data), input_locations)
    )

    output = data.iloc[result_ids][["msec", "subject", "trial"]].to_dict("records")

    Path("output.json").write_text(json.dumps(output))
