import pandas as pd
from sklearn.neighbors import KDTree
import pickle

data = pd.read_csv("data.csv")

data = data.loc[data["entity_id"] == 0].drop_duplicates().reset_index()
data.to_pickle("data.pkl")

pos_cols = [f"{ax}_position" for ax in ["x", "y", "z"]]

data_subset = (
    pd.read_csv("data.csv")[lambda _df: _df["keycode"] == "p"]
    .drop_duplicates(subset=["msec", "subject", "trial"])
    .dropna()
    .reset_index()
)

pos_cols = [f"{ax}_position" for ax in ["x", "y", "z"]]

tree = KDTree(data_subset.loc[:, pos_cols].to_numpy(), leaf_size=1)

data_subset.to_parquet("data_subset.parquet")

with open("kdtree.pickle", "wb") as file:
    pickle.dump(tree, file)