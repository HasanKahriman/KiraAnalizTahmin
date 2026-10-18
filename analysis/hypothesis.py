import numpy as np
from scipy import stats

def price_furniture_difference_test(cursor,alpha=0.05):
    cursor.execute("SELECT price,furniture FROM Rental_listing")
    rows=cursor.fetchall()

    if not rows:
        raise ValueError("No data found!")

    furniture_price=np.array([price for price, furniture in rows if furniture == True])
    not_furniture_price=np.array([price for price, furniture in rows if furniture == False])

    furniture_mean=furniture_price.mean()
    not_furniture_mean=not_furniture_price.mean()

    _, p_levene = stats.levene(furniture_price, not_furniture_price)
    has_equal_var = p_levene >= alpha
    t_stat, p_value = stats.ttest_ind(furniture_price, not_furniture_price, equal_var=has_equal_var)

    h0_rejected = bool(p_value < alpha)
    print("----- HYPOTHESIS TEST RESULTS -----")
    print(f"H0: Price means are the same")
    print(f"H1: Price means are different")
    if h0_rejected:
        comment="Reject null hypothesis.\nThere is a difference between the means of prices furnished and unfurnished house prices."
    else:
        comment="Fail to reject null hypothesis.\nThere is no difference between the means of prices furnished and unfurnished house prices."

    return {
        "Property house price mean": round(furniture_mean,2),
        "The price of a detached house mean":round(not_furniture_mean,2),
        "t-statistic": round(t_stat,4),
        "p-value": p_value,
        "p_levene": p_levene,
        "h0_rejected":h0_rejected,
        "Comment":comment
    }

def price_house_age_difference_test(cursor,alpha=0.05):
    cursor.execute("SELECT price,house_age FROM Rental_listing")
    rows=cursor.fetchall()

    if not rows:
        raise ValueError("No data found!")

    new_house=np.array([price for price, house_age in rows if house_age <=5])
    old_house=np.array([price for price, house_age in rows if house_age >5])

    new_house_mean=new_house.mean()
    ols_house_mean=old_house.mean()

    _, p_levene = stats.levene(new_house, old_house)
    has_equal_var = p_levene >= alpha
    t_stat, p_value = stats.ttest_ind(new_house, old_house, equal_var=has_equal_var)

    h0_rejected = bool(p_value < alpha)
    print("----- HYPOTHESIS TEST RESULTS -----")
    print(f"H0: Price means are the same")
    print(f"H1: Price means are different")
    if h0_rejected:
        comment="Reject null hypothesis.\nThere is a difference between the means of prices the old houses and the new houses."
    else:
        comment="Fail to reject null hypothesis.\nThere is no difference between the means of prices the old houses and the new houses."

    return {
        "New house price mean": round(new_house_mean,2),
        "Old house price mean":round(ols_house_mean,2),
        "t-statistic": round(t_stat,4),
        "p-value": p_value,
        "p_levene": p_levene,
        "h0_rejected":h0_rejected,
        "Comment":comment
    }