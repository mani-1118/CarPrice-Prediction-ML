import pandas as pd
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline

from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor

from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error


# 1. Load dataset
data = pd.read_csv("car data.csv")

print("Dataset shape:", data.shape)
print("\nColumns:")
print(data.columns.tolist())


# 2. Select features and target
X = data.drop("Selling_Price", axis=1)
y = data["Selling_Price"]


# 3. Identify categorical and numerical columns
categorical_features = [
    "Car_Name",
    "Fuel_Type",
    "Seller_Type",
    "Transmission"
]

numerical_features = [
    "Year",
    "Present_Price",
    "Kms_Driven",
    "Owner"
]


# 4. Preprocessing
preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        ),
        (
            "numerical",
            "passthrough",
            numerical_features
        )
    ]
)


# 5. Split data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# 6. Create models
models = {
    "Linear Regression": LinearRegression(),

    "Decision Tree": DecisionTreeRegressor(
        random_state=42
    ),

    "Random Forest": RandomForestRegressor(
        n_estimators=200,
        random_state=42
    )
}


# 7. Train and evaluate models
results = {}

for name, model in models.items():

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", model)
        ]
    )

    pipeline.fit(X_train, y_train)

    predictions = pipeline.predict(X_test)

    r2 = r2_score(y_test, predictions)
    mae = mean_absolute_error(y_test, predictions)
    rmse = mean_squared_error(
        y_test,
        predictions
    ) ** 0.5

    results[name] = {
        "R2": r2,
        "MAE": mae,
        "RMSE": rmse
    }

    print("\n" + "=" * 45)
    print(name)
    print("=" * 45)
    print("R2 Score :", round(r2, 4))
    print("MAE      :", round(mae, 4))
    print("RMSE     :", round(rmse, 4))


# 8. Find best model based on R2
best_model_name = max(
    results,
    key=lambda x: results[x]["R2"]
)

print("\n" + "=" * 45)
print("BEST MODEL")
print("=" * 45)
print(best_model_name)
print("R2:", round(results[best_model_name]["R2"], 4))


# 9. Train the best model again on the complete dataset
best_model = models[best_model_name]

final_pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", best_model)
    ]
)

final_pipeline.fit(X, y)


# 10. Create models folder
os.makedirs("models", exist_ok=True)


# 11. Save final model
joblib.dump(
    final_pipeline,
    "models/car_price_model.pkl"
)

print("\nFinal model saved successfully!")
print("Location: models/car_price_model.pkl")