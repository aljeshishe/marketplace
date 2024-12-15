import pandas as pd

def filter_in(df, query: str) -> pd.DataFrame:
    found = df.query(query)
    print(f"removing {len(df) - len(found)} rows")
    return found
