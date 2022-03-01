import pandas as pd
import json
from pathlib import Path



if __name__ == "__main__":

    def get_distance_index_t(query, row):
        distance = [sum([(query[k] - row[i]["coord"][k]) ** 2 for k in [0,1,2]]) ** 0.5 for i in range(len(row))]# kiszámolja a távolságot
        return distance.index(min(distance))

    data = pd.read_pickle("data.pkl")
    data["coord"] = data[["x_position", "y_position", "z_position"]].apply(tuple, axis = 1)
    data = data.loc[:,["msec","coord","subject","trial"]]
    dict_df = data.to_dict('records')
    input_locations = json.loads(Path("input.json").read_text())
    input = {i: tuple(input_locations[i].values()) for i in range(len(input_locations))}

    distance = [get_distance_index_t(input[i], dict_df) for i in range(len(input))]

    results = data.iloc[distance,[0,-2,-1]].to_dict("records")
    Path("output.json").write_text(json.dumps(results))