import pandas as pd
from database.db_manager import DatabaseManager
from prediction import interactive_prediction
from src.data_cleaning import handling_missing_values,handling_outliers,convert_to_numeric
from analysis.statistics import calculate_rent_price_statistics
from analysis.hypothesis import price_furniture_difference_test,price_house_age_difference_test
from src.eda_featuring import add_new_features
from src.encoding import apply_encoding
from src.model_training import train_and_evaluate_linear_model,train_and_evaluate_polynomial_model
from src.report import generate_final_report

df=pd.read_csv("data/train.csv")
df=handling_missing_values(df)
df=convert_to_numeric(df)
df=handling_outliers(df)
db=DatabaseManager()
db.create_tables()
add_new_features(db)
conn=db.get_connection()
cursor=conn.cursor()

questions = {
    "1. Ankara'daki ortalama kira ne?": """
    SELECT ROUND(AVG(price), 2) AS average_price FROM Rental_listing WHERE city="Ankara";
    """,
    "2. İlçelere göre ortalama kira nedir?": """
    SELECT town, ROUND(AVG(price), 2) AS average_price FROM Rental_listing GROUP BY town ORDER BY average_price DESC;
    """,
    "3. En pahalı 10 ilan hangisi?": """
    SELECT * FROM Rental_listing ORDER BY price DESC LIMIT 10;
    """,
    "4. 100 m² üzerindeki evlerin ortalama kirası nedir?": """
    SELECT ROUND(AVG(price), 2) AS average_price FROM Rental_listing WHERE house_size > 100;
    """,
    "5. Eşyalı ve eşyasız evlerin ortalama kiraları nedir?": """
    SELECT furniture, ROUND(AVG(price), 2) AS average_price FROM Rental_listing GROUP BY furniture;
    """,
    "6. Oda sayısına göre ortalama kira nedir?": """
    SELECT room_count, ROUND(AVG(price), 2) AS average_price FROM Rental_listing GROUP BY room_count ORDER BY average_price DESC;
    """,
    "7. En fazla ilan bulunan ilçeler hangileri?": """
    SELECT town, COUNT(*) AS ilan_sayisi FROM Rental_listing GROUP BY town ORDER BY ilan_sayisi DESC;
    """,
    "8. Bina yaşı 5'ten küçük evlerin ortalama kira fiyatı nedir?": """
    SELECT ROUND(AVG(price), 2) AS average_price FROM Rental_listing WHERE house_age < 5;
    """
}

for question,answer in questions.items():
    print(f"\n---{question}---")
    result_df=db.execute_query(answer)
    print(result_df)

price_statistics=calculate_rent_price_statistics(cursor)
print("\n--- Kira Fiyat İstatistikleri ---")
for key, value in price_statistics.items():
    print(f"{key}: {value}")

print()

furniture_hypothesis=price_furniture_difference_test(cursor)
print("\n--- Eşyalı ve Eşyasız Ev Fiyatı Arasında Fark Var mı? ---")
for key, value in furniture_hypothesis.items():
    print(f"{key}: {value}")

print()

house_age_hypothesis=price_house_age_difference_test(cursor)
print("\n--- Yeni ve Eski Evler Arasında Fiyat Farkı Var mı? ---")
for key, value in house_age_hypothesis.items():
    print(f"{key}: {value}")

df = db.execute_query("SELECT * FROM Rental_listing")
df.drop(columns=["floor","list_id","price_per_m2"], inplace=True)
report_df=df
df=apply_encoding(df)
print("-" * 40)
print("LINEAR MODEL")
regressor,scaler,columns,means,linear_r2=train_and_evaluate_linear_model(df)
print("-" * 40)

for d in [1,2]:
    print(f"POLYNOMIAL MODEL({d})")
    poly_model,poly_scaler,poly,poly_r2=train_and_evaluate_polynomial_model(df,target_col="price",degree=d)

choice=""
print("-" * 40)
print("----- HOME RENT FORECASTING SYSTEM -----")
while choice!="0":
    print("=" * 40)
    print("0-QUIT")
    print("1-PREDICTION")
    choice=input("Enter your choice: ")
    if choice=="1":
        interactive_prediction(regressor, scaler, columns, means)

generate_final_report(report_df,regressor,columns,linear_r2,poly_r2)

conn.close()

