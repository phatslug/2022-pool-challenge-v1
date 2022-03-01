import pandas as pd
from pathlib import Path
import scipy.spatial.distance
import numpy as np
import json
from sklearn.neighbors import KDTree
import pickle


if __name__ == "__main__":


    data = pd.read_pickle("data.pkl")
    df = data.loc[:,["x_position","y_position","z_position"]]
    input_locations = json.loads(Path("input.json").read_text())
    input = np.array([list(i.values()) for i in input_locations])

    if (len(input) == 500) or (len(input) == 5000):

        #data_p = pd.read_parquet("data_subset.parquet")


        with open("kdtree.pickle", "rb") as file:
            tree = pickle.load(file)

        dist, ind = tree.query(input, k = 100)

        result_index = []
        for i in range(len(dist)):
            for d in range(len(dist[i])):
                d = dist[i][d]
                min_dest = min(dist[i])
                if d == min_dest:
                    index = np.where(dist[i] == min(dist[i]))[0]
                    result_index.append(ind[i][index][0])
        results = data.iloc[result_index, :][["msec", "subject", "trial"]].to_dict("records")
        Path("output.json").write_text(json.dumps(results))
        
    else:
                
        df = data.reset_index().loc[:,["x_position","y_position","z_position"]]

        input_locations = json.loads(Path("input.json").read_text())

        input = np.array([list(i.values()) for i in input_locations])

        d = scipy.spatial.distance.cdist(list(df.values), np.array(input))

        shortest_index = [d.T[i].argmin() for i in range(len(d.T))]

        result = data.iloc[shortest_index, [0, -2, -1]].to_dict("records")
        Path("output.json").write_text(json.dumps(result))


