import pandas as pd
from collections import Counter

def counter_to_df(counter: Counter, col_name: str) -> pd.DataFrame:
    return pd.Series(counter)\
             .sort_values(ascending=False)\
             .reset_index()\
             .rename(columns={"index": col_name, 0: "count"})

def list_to_df(values: list, column_name: str) -> pd.DataFrame:
    return pd.DataFrame(values, columns=[column_name])
