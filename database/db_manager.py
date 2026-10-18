import sqlite3
import pandas as pd

class DatabaseManager:
    def __init__(self, db_path="database/real_estate.db"):
        self.db_path = db_path

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def create_tables(self):
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS Rental_listing(
                          list_id INTEGER PRIMARY KEY AUTOINCREMENT,
                          city TEXT,
                          town TEXT,
                          neighborhood TEXT,
                          apartment_type TEXT,
                          house_type TEXT,
                          house_age INTEGER,
                          house_size INTEGER,
                          room_count TEXT,
                          floor TEXT,
                          furniture BOOLEAN,
                          bathroom_count INTEGER,
                          hand TEXT,
                          heater_type TEXT,
                          heater_fuel TEXT,
                          price INTEGER
                          )
                       """)

        conn.commit()
        conn.close()
        print("The database and table were created successfully.")

    def import_data_from_csv(self, df: pd.DataFrame):
        df = df.copy()

        # Sadece veritabanı tablosunda olan 15 sütunu seçiyoruz (list_id veya Unnamed: 0 varsa elenir)
        valid_columns = [
            "city", "town", "neighborhood", "apartment_type", "house_type",
            "house_age", "house_size", "room_count", "floor", "furniture",
            "bathroom_count", "hand", "heater_type", "heater_fuel", "price"
        ]
        df = df[[col for col in valid_columns if col in df.columns]]

        conn = self.get_connection()
        try:
            conn.execute("DELETE FROM Rental_listing")
            conn.commit()
            df.to_sql("Rental_listing", con=conn, if_exists="append", index=False)
            conn.commit()
            print(f"Veri aktarımı başarıyla tamamlandı! ({len(df)} satır eklendi)")
        except Exception as e:
            # Gerçek hatayı tam olarak ekrana yazdırır:
            print(f"GERÇEK HATA SEBEBİ: {repr(e)}")
        finally:
            conn.close()

    def execute_query(self, query: str):
        with self.get_connection() as conn:
            return pd.read_sql_query(query, conn)

    def execute_update(self,query: str):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(query)
            conn.commit()
        except sqlite3.OperationalError as e:
            pass
        finally:
            conn.close()