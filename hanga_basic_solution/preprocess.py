import pandas as pd


if __name__ == "__main__":

    raw_data = pd.read_csv("data.csv")
    filtered_data = raw_data.loc[lambda df: df["keycode"] == "p"].drop_duplicates()
    filtered_data.to_parquet("filtered_data.parquet")
    