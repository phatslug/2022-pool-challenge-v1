import pandas as pd

df = pd.read_csv("data.csv")
df.drop(["entity_id"], inplace=True, axis=1)
df.drop(df[df['keycode']!="p"].index, inplace=True)
df=df.drop_duplicates().dropna().reset_index(drop = True)