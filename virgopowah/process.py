import pandas as pd
import numpy as np
import pickle
from sklearn.neighbors import BallTree
import json
from pathlib import Path



if __name__ == "__main__":

    with open('treesave.pkl', 'rb') as handle:
        tree = pickle.load(handle)

    input_locations = json.loads(Path("input.json").read_text())
    
    
    input = np.array([list(i.values()) for i in input_locations])

    dist, ind = tree.query(input, k = 100)
    indexes = [ind[i][0] for i in range(len(ind))]

    data = pd.read_pickle("data.pkl")
    own_results = data.iloc[indexes,[1,-2,-1]].to_dict("records")
    Path("output.json").write_text(json.dumps(own_results))