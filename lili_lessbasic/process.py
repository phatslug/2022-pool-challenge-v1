from pathlib import Path
import json
import pandas as pd

if __name__ == "__main__":
    df = pd.read_pickle("data.pkl")
    ydict = df.to_dict('index')
    input_locations = json.loads(Path("input.json").read_text())

    def get_distance(row, query):
        keys = [f"{ax}_position" for ax in ["x", "y", "z"]] # oszlopok nevei
        return sum([(row[k] - query[k]) ** 2 for k in keys]) ** 0.5 # kiszámolja a távolságot

    fkeys = ["msec", "subject", "trial"]

    out = []
    for input_place in input_locations: # végigiterál az oszlopokon
        min_dist = float("inf") 
        closest = {}
        for key in ydict:
            if ydict.get(key)['keycode'] == 'p':
                distance = get_distance(ydict.get(key), input_place)
                if distance < min_dist:
                    min_dist = distance
                    closest["msec"] = ydict.get(key)["msec"]
                    closest["subject"] = ydict.get(key)["subject"]
                    closest["trial"] = ydict.get(key)["trial"]
        out.append(closest)
    
    Path("output.json").write_text(json.dumps(out))