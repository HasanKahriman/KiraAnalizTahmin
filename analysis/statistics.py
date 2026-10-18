import pandas as pd

def calculate_rent_price_statistics(cursor):
    query="SELECT price FROM Rental_listing WHERE price IS NOT NULL"
    cursor.execute(query)

    df=pd.DataFrame(cursor.fetchall(),columns=['price'])

    if df.empty:
        return "No data"

    median=round(df['price'].median(),2)
    mean=round(df['price'].mean(),2)
    std=round(df['price'].std(),2)
    variance=round(df['price'].var(),2)
    minimum=df['price'].min()
    maximum=df['price'].max()
    quartile_1=df['price'].quantile(0.25)
    quartile_3=df['price'].quantile(0.75)

    if mean > median:
        comment="Fiyatı çok fazla olan evler olduğu için ortalama medyandan daha yüksek."
    elif mean < median:
        comment="Fiyatı çok az olan evler olduğu için ortalama medyandan daha düşük."
    else:
        comment="Medyan ve ortalama eşit. Dengeli fiyatlar var."

    return {
        "median":median,
        "mean":mean,
        "std":std,
        "variance":variance,
        "minimum":minimum,
        "maximum":maximum,
        "quartile_1":quartile_1,
        "quartile_3":quartile_3,
        "comment":comment
    }

