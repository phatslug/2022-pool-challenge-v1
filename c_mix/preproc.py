import pandas as pd
import json

pos_cols = [f"{ax}_position" for ax in ["x", "y", "z"]]
out_cols = ["msec", "subject", "trial"]

dfo = (
    pd.read_csv("data.csv")
    .loc[lambda df: df["entity_id"] == 0, [*pos_cols, *out_cols]]
    .dropna(how="any")
    .drop_duplicates(subset=out_cols)
    .drop_duplicates(subset=pos_cols)
    .assign(dicstr=lambda df: [*map(json.dumps, df[out_cols].to_dict("records"))])
)

dfo[[*pos_cols, "dicstr"]].to_csv("to-c.csv", index=False, header=False, sep=";", quotechar="'")