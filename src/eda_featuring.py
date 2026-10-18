import pandas as pd

def add_new_features(db):
    alter_query0="ALTER TABLE Rental_listing ADD COLUMN price_per_m2 REAL;"
    db.execute_update(alter_query0)

    update_query0="""
    UPDATE Rental_listing
    SET price_per_m2=ROUND((price*1.0)/(house_size),2)
    WHERE house_size>0;
    """
    db.execute_update(update_query0)

    alter_query1="ALTER TABLE Rental_listing ADD COLUMN building_age_category TEXT;"
    db.execute_update(alter_query1)

    update_query1="""
    UPDATE Rental_listing
    SET building_age_category=CASE
        WHEN house_age >=0 AND house_age <= 5 THEN 'Yeni'
        WHEN house_age >=6 AND house_age <= 15 THEN 'Orta'
        WHEN house_age >=16 AND house_age <= 30 THEN 'Eski'
        WHEN house_age >30 THEN 'Çok eski'
        ELSE 'Bilinmiyor'
    END;
    """
    db.execute_update(update_query1)
    print("Yeni özellikler (price_per_m2,building_age_category) veritabanına başarıyla eklendi.")