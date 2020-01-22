import pandas as pd


def partialMatch(df: pd.DataFrame, field, string):
    return df[df[field].contains(string)]


def perfectMatch(df: pd.DataFrame, field, string):
    result = df[df[field] == string]
    if result.empty:
        return None
    else:
        return result
