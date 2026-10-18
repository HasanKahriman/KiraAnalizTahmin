import pandas as pd
import numpy as np

def handling_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    df=df.copy()
    cols=["floor","furniture","hand","heater_fuel"]
    for col in cols:
        df[col]=df[col].fillna(df[col].mode()[0])
    df["bathroom_count"]=df["bathroom_count"].fillna(df["bathroom_count"].median())
    return df

def convert_to_numeric(df: pd.DataFrame) -> pd.DataFrame:
    df=df.copy()
    cols=["house_age","house_size"]
    df["house_age"]=df["house_age"].str.replace("Sıfır","0")
    df["house_size"]=df["house_size"].str.replace(" m2","").str.replace(".","",regex=False)

    for col in cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=cols)
    for col in cols:
        df[col]=df[col].astype(int)
    return df

def handling_outliers(df: pd.DataFrame) -> pd.DataFrame:
    df=df.copy()
    conditions=(
        (df["bathroom_count"] <= 10)
        & (df["house_age"] < 45)
        & (df["house_size"] > 0)
        & (df["price"] < 2_000_000)
    )
    df=df[conditions]
    return df


