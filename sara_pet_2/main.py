from scipy import spatial
from pathlib import Path
import json
import pandas as pd

if __name__ == "__main__":

    df = pd.read_pickle("df.pkl")
    input_locations = json.loads(Path("input.json").read_text())

    tree = spatial.KDTree(df[["x_position","y_position","z_position"]],leafsize=20)
    eredmeny=[]

    for i in range(0,len(input_locations)):
        dd, ii = tree.query(list(input_locations[i].values()),k=100)
        eredmeny.append(df[["msec","subject","trial"]].iloc[min(zip(dd,ii))[1]].to_dict())
    Path("output.json").write_text(json.dumps(eredmeny))