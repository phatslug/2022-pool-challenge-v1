from scipy import spatial
from pathlib import Path
import json
import pandas as pd

if __name__ == "__main__":

    input_locations = json.loads(Path("input.json").read_text())

    tree = spatial.KDTree(df.loc[df["keycode"] == "p", ["x_position","y_position","z_position"]])
    eredmeny=[]

    for i in range(0,len(input_locations)):
        dd, ii = tree.query(list(input_locations[i].values()))
        eredmeny.append(df.loc[df["keycode"] == "p",["msec","subject","trial"]].iloc[ii].to_dict())
    Path("output.json").write_text(json.dumps(eredmeny))