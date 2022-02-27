import pandas as pd

data = pd.read_csv("data.csv")
data = data.loc[data["entity_id"] == 0].drop_duplicates().reset_index()
data.to_pickle("data.pkl")