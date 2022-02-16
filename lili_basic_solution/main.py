from pathlib import Path
import json

import pandas as pd

def get_distance(row, query):
    keys = [f"{ax}_position" for ax in ["x", "y", "z"]]
    return sum([(row[k] - query[k]) ** 2 for k in keys]) ** 0.5


if __name__ == "__main__":

    df = pd.read_csv("data.csv")
    input_locations = json.loads(Path("input.json").read_text())
    fkeys = ["msec", "subject", "trial"]

    out = []
    for input_place in input_locations:
        min_dist = float("inf")
        closest = {}
        for ind, row in df.loc[df["keycode"] == "p", :].iterrows():
            distance = get_distance(row, input_place)
            if distance < min_dist:
                min_dist = distance
                closest = row[fkeys].to_dict()
        out.append(closest)