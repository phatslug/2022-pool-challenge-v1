from fastapi import FastAPI
import pandas as pd
from sklearn.neighbors import KDTree
from pydantic import BaseModel
from typing import List
import numpy as np
import uvicorn

app = FastAPI()

result_data = (
    pd.read_csv("data.csv")[lambda _df: _df["keycode"] == "p"]
    .drop_duplicates(subset=["msec", "subject", "trial"])
    .dropna()
    .reset_index()
)

pos_cols = [f"{ax}_position" for ax in ["x", "y", "z"]]

kdtree = KDTree(result_data.loc[:, pos_cols].to_numpy(), leaf_size=1)


class Item(BaseModel):
    x_position: float
    y_position: float
    z_position: float


class ItemList(BaseModel):
    __root__: List[Item]


def process_input(input_json):
    return np.array([tuple(pos.values()) for pos in input_json], dtype=np.float32)


def get_entity(t_index: int):
    return result_data.iloc[t_index, :][["msec", "subject", "trial"]].to_dict("records")


@app.post("/")
def get_index(input_json: ItemList):
    dist, ind = kdtree.query(process_input(input_json.dict()["__root__"]), k=10)
    results_index = [
        min([i for d, i in zip(d_vec, i_vec) if d == d_vec.min()])
        for d_vec, i_vec in zip(dist, ind)
    ]
    return get_entity(results_index)

@app.get('/szarosapi')
def szar():
    return 'Élek'

if __name__ == "__main__":
    uvicorn.run("fastapi_app:app", proxy_headers = True, debug = True)