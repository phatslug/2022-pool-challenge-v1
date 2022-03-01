import pandas as pd
from sklearn.neighbors import KDTree
import pickle
import numpy as np

data = pd.read_csv("data.csv")

cols_1 = ['msec', 'x_position', 'y_position', 'z_position', 'subject', 'trial']
cols = ["x_position","y_position","z_position"]

data = data.loc[data["entity_id"] == 0].drop_duplicates(["msec","trial","subject"]).dropna().reset_index(drop = True)
data = data.loc[:,cols_1]

for i in ["x_position", "y_position","z_position"]:
    data[i] = data[i].astype(np.float32)

data["msec"] = data["msec"].astype(np.int32)
data["trial"] = data["trial"].astype(np.int8)
data["subject"] = data["subject"].astype("category")

data.to_pickle("data.pkl")

tree = KDTree(data.loc[:, ["msec", "trial","subject"]].to_numpy(), leaf_size=1)

with open("kdtree.pickle", "wb") as file:
        pickle.dump(tree, file)