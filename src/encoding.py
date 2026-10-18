import pandas as pd

def apply_encoding(df: pd.DataFrame) -> pd.DataFrame:
    df=df.copy()

    df=clean_room_count(df)

    for col in ["city","town","neighborhood"]:
        col_mean=df.groupby(col)['price'].mean()
        df[f"{col}_encoded"]=df[col].map(col_mean)
        df.drop(columns=[col],inplace=True)


    df['hand']=df['hand'].map({"Sıfır":0,"İkinci El":1,"Betonarme":2})
    age_mapping={"Yeni":4,"Orta":3,"Eski":2,"Çok eski":1,"Bilinmiyor":0}
    df['building_age_category']=df['building_age_category'].map(age_mapping)
    columns_to_one_hot=['heater_type','heater_fuel','apartment_type','house_type']
    df=pd.get_dummies(df,columns=columns_to_one_hot,drop_first=True)
    return df


def clean_room_count(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if "room_count" in df.columns:
        # '3 + 1' gibi ifadeleri parçalayıp sayısal toplama dönüştürüyoruz (Örn: 3 + 1 = 4)
        # Eğer sadece ilk sayıyı almak istersen str[0] da yapabilirsin.
        def parse_rooms(val):
            if pd.isna(val):
                return 0
            val_str = str(val)
            if "+" in val_str:
                parts = val_str.split("+")
                try:
                    return float(parts[0].strip()) + float(parts[1].strip())
                except:
                    return 0
            try:
                return float(val_str)
            except:
                return 0

        df["room_count"] = df["room_count"].apply(parse_rooms)

    return df