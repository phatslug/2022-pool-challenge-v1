import pandas as pd
from sklearn.neighbors import KDTree
import pickle

data_subset = (
    pd.read_csv("data.csv")[lambda _df: _df["entity_id"] == 0]
    .drop_duplicates(subset=["msec", "subject", "trial"])
    .reset_index()
)

pos_cols = [f"{ax}_position" for ax in ["x", "y", "z"]]

tree = KDTree(data_subset.loc[:, pos_cols].to_numpy(), leaf_size=1)

data_subset.to_parquet("data_subset.parquet")

with open("kdtree.pickle", "wb") as file:
    pickle.dump(tree, file)
