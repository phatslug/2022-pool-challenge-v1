import pandas as pd
from sklearn.neighbors import KDTree
import pickle

data_subset = (
    pd.read_csv("data.csv")[lambda _df: _df["keycode"] == "p"]
    .drop_duplicates(subset=["msec", "subject", "trial"])
    .dropna()
    .reset_index()
)

pos_cols = [f"{ax}_position" for ax in ["x", "y", "z"]]

tree = KDTree(data_subset.loc[:, pos_cols].to_numpy(), leaf_size=1)
#tree_1 = KDTree(data_subset.loc[:, pos_cols].to_numpy(), leaf_size=16) # if query == 10
#tree_2 = KDTree(data_subset.loc[:, pos_cols].to_numpy(), leaf_size=38) # if query == 500 or higher

#data_subset = data_subset.loc[:,["msec", 'x_position', 'y_position', 'z_position', "subject", "trial"]]

data_subset.to_parquet("data_subset.parquet")

with open("kdtree.pickle", "wb") as file:
        pickle.dump(tree, file)