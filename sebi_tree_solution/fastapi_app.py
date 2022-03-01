from fastapi import FastAPI
import pandas as pd
from sklearn.neighbors import KDTree
from pydantic import BaseModel
from typing import List
import numpy as np
import uvicorn
import json
from pathlib import Path
import os
import signal

app = FastAPI()

result_data = (
    pd.read_csv("data.csv")[lambda _df: _df["keycode"] == "p"]
    .drop_duplicates(subset=["msec", "subject", "trial"])
    .dropna()
    .reset_index()
)

pos_cols = [f"{ax}_position" for ax in ["x", "y", "z"]]

kdtree = KDTree(result_data.loc[:, pos_cols].to_numpy(), leaf_size=1, metric = "euclidean")

result_data.drop(columns = ['index', 'keycode', 'entity_id', *pos_cols], inplace=True)

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

def read_input() -> dict:
    return json.loads(Path("input.json").read_text())


def write_results(results):
    Path("output.json").write_text(json.dumps(results))

@app.get("/megoldas")
def get_index():
    dist, ind = kdtree.query(process_input(read_input()), k=10)
    results_index = [
        min([i for d, i in zip(d_vec, i_vec) if d == d_vec.min()])
        for d_vec, i_vec in zip(dist, ind)
    ]
    write_results(get_entity(results_index))
    print('Kész vok')

@app.get('/szarosapi')
def szar():
    return 'Élek'

@app.get('/kill_me')
def kill_proc():
    os.kill(int(Path('process_data.txt').read_text()), signal.SIGTERM) #or signal.SIGKILL 

if __name__ == "__main__":
    uvicorn.run("fastapi_app:app", port = 8099, proxy_headers = True, debug = True)