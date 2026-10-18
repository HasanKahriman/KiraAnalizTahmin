import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error,mean_absolute_error,r2_score
from sklearn.preprocessing import StandardScaler,PolynomialFeatures

def train_and_evaluate_linear_model(df: pd.DataFrame,target_col="price"):
    X=df.drop(columns=[target_col])
    y=df[target_col]
    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,random_state=42)
    scaler=StandardScaler()
    X_train_scaled=scaler.fit_transform(X_train)
    X_test_scaled=scaler.transform(X_test)
    regressor=LinearRegression()
    regressor.fit(X_train_scaled,y_train)
    print("-" * 40)
    coefficients = pd.DataFrame({
        'Variable': X.columns,
        'Coefficients': regressor.coef_
    })
    coefficients = coefficients.sort_values(by='Coefficients', ascending=False)
    print(coefficients)
    print("-" * 40)
    y_pred=regressor.predict(X_test_scaled)

    mae=mean_absolute_error(y_test,y_pred)
    mse=mean_squared_error(y_test,y_pred)
    r2=r2_score(y_test,y_pred)

    print(f"MAE: {mae:.2f}")
    print(f"MSE: {mse:.2f}")
    print(f"R2 score: {r2:.4f}")

    return regressor,scaler,X.columns,X.mean(),r2

def train_and_evaluate_polynomial_model(df: pd.DataFrame,target_col="price",degree=2):
    X=df.drop(columns=[target_col])
    y=df[target_col]
    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,random_state=42)
    scaler=StandardScaler()
    X_train_scaled=scaler.fit_transform(X_train)
    X_test_scaled=scaler.transform(X_test)
    poly = PolynomialFeatures(degree=degree, include_bias=False)
    X_train_poly = poly.fit_transform(X_train_scaled)
    X_test_poly = poly.transform(X_test_scaled)
    regressor=LinearRegression()
    regressor.fit(X_train_poly,y_train)
    y_pred=regressor.predict(X_test_poly)

    mae=mean_absolute_error(y_test,y_pred)
    mse=mean_squared_error(y_test,y_pred)
    r2=r2_score(y_test,y_pred)

    print(f"MAE: {mae:.2f}")
    print(f"MSE: {mse:.2f}")
    print(f"R2 score: {r2:.4f}")

    return regressor,scaler,poly,r2

