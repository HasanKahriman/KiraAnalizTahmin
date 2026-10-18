import pandas as pd

def interactive_prediction(model,scaler,feature_columns,feature_means):
    print("\n" + "="*40)
    print("USER INPUT:HOUSE INFORMATION")
    print("=" * 40)

    try:
        house_size=float(input("M2: "))
        house_age=float(input("House Age: "))
        bathroom_count=float(input("Bathroom Count: "))
        furniture_input=input("Furniture Input(True/False): ")
        furniture = 1 if furniture_input=="True" else 0

        input_data=feature_means.to_dict()

        if "house_size" in input_data: input_data["house_size"]=house_size
        if "house_age" in input_data: input_data["house_age"] = house_age
        if "bathroom_count" in input_data: input_data["bathroom_count"] = bathroom_count
        if "furniture" in input_data: input_data["furniture"] = furniture

        df_input=pd.DataFrame([input_data])
        scaled_input=scaler.transform(df_input)
        model_prediction=model.predict(scaled_input)
        prediction=float(model_prediction[0])

        print("---------------------------------")
        print(f"Estimated Rent: {prediction:,.0f} TL / Month")
        print(f"House size: {house_size} m²")
        print("---------------------------------\n")
    except ValueError:
        print("Error. Please enter a numeric value.")


