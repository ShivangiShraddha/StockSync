import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error


def forecast_demand(df):

    results = {}

    products = df["product_name"].unique()

    for product in products:

        product_df = df[df["product_name"] == product].copy()

        product_df["time_index"] = range(len(product_df))
        product_df["day_of_week"] = product_df["date"].dt.dayofweek
        product_df["month"] = product_df["date"].dt.month

        product_df["lag_1"] = product_df["quantity_sold"].shift(1)
        product_df["lag_2"] = product_df["quantity_sold"].shift(2)
        product_df["lag_3"] = product_df["quantity_sold"].shift(3)
        product_df["lag_7"] = product_df["quantity_sold"].shift(7)
        product_df["lag_14"] = product_df["quantity_sold"].shift(14)
        product_df["lag_30"] = product_df["quantity_sold"].shift(30)

        product_df = product_df.dropna()

        features = [
            "lag_1", "lag_2", "lag_3",
            "lag_7", "lag_14", "lag_30",
            "day_of_week", "month",
            "time_index"
        ]

        X = product_df[features]
        y = product_df["quantity_sold"]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, shuffle=False
        )

        model = RandomForestRegressor(n_estimators=200, random_state=42)

        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)

        mae = mean_absolute_error(y_test, y_pred)

        predicted_demand = int(round(product_df["quantity_sold"].mean()))

        results[product] = {
            "MAE": round(mae, 2),
            "Predicted Daily Demand": predicted_demand
        }

    return results