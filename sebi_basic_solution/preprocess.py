import pandas as pd

data_subset = pd.read_csv("data.csv")[
    lambda _df: _df["entity_id"] == 0
].drop_duplicates(subset=["msec", "subject", "trial"])

data_subset.to_parquet("data_subset.parquet")
