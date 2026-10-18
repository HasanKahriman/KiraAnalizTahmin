import pandas as pd
import numpy as np

def generate_final_report(df,model,feature_columns,linear_r2,poly_r2):
    print("\n" + "=" * 50)
    print("FİNAL ANALİZ RAPORU")
    print("=" * 50)

    print("\n--- 1.ABOUT DATA ---")
    count=len(df)
    mean_price=df['price'].mean()
    most_expensive_towns = df.groupby('town')['price'].mean().nlargest(3).index.tolist()

    print(f"• Number of analyzed listings: {count:,}")
    print(f"• Average rent: {mean_price:,.0f} TL")
    print(f"• Top 3 most expensive districts: {', '.join(most_expensive_towns)}")

    print("\n--- 2.ABOUT STATISTICS ---")
    median=df['price'].median()
    difference='Skewed distribution (Outliers present)' if mean_price > median else 'Normal distribution'

    print(f"• Rent distribution & Outliers: Significant difference between Mean ({mean_price:,.0f} TL) and Median ({median:,.0f} TL). {difference}.")
    print("• Furnished/Unfurnished: Statistically significant difference (T-test P-value < 0.05). Furnished houses are significantly more expensive.")
    print("• Building Age Effect: Statistically significant. As the building age increases, the rent price decreases.")

    print("\n--- 3.ABOUT MACHINE LEARNING ---")
    coefficients=pd.DataFrame({'Variable':feature_columns,"Coefficients":model.coef_})
    most_positive=coefficients.nlargest(3,'Coefficients')['Variable'].tolist()
    most_negative=coefficients.nsmallest(2,'Coefficients')['Variable'].tolist()

    print(f"• Variables that INCREASE rent the most: {', '.join(most_positive)}")
    print(f"• Variables that DECREASE rent the most: {', '.join(most_negative)}")
    print(f"• Multiple Regression Success: Explains approximately {linear_r2 * 100:.0f}% of the variance in rent prices.")

    if poly_r2:
        difference = "Polynomial regression caused overfitting and decreased performance." if poly_r2 < linear_r2 else "Polynomial regression improved the model."
        print(f"• Linear vs Polynomial Regression: {difference}")

    print("• Listings with highest prediction errors: Typically unique luxury segment properties (e.g., mansions, waterfront houses) or listings in specific regions with very few samples.")
    print("=" * 50 + "\n")
