def detect_expiry(df, forecast_results):

    expiry_results = {}

    # Example shelf life (days) per product
    shelf_life_catalog = {
        "Rice": 365,
        "Oil": 365,
        "Sugar": 365,
        "Milk": 7,
        "Soap": 730
    }

    products = forecast_results.keys()

    for product in products:

        predicted_daily_demand = forecast_results[product]["Predicted Daily Demand"]

        shelf_life_days = shelf_life_catalog.get(product, 30)

        current_stock = int(
            df[df["product_name"] == product]["current_stock"].iloc[-1]
        )

        # Maximum units that can be sold before expiry
        possible_sales = predicted_daily_demand * shelf_life_days

        if current_stock > possible_sales:
            expiry_risk = current_stock - possible_sales
            status = "Expiry Risk"
        else:
            expiry_risk = 0
            status = "Safe"

        expiry_results[product] = {
            "Shelf Life (days)": shelf_life_days,
            "Current Stock": current_stock,
            "Possible Sales Before Expiry": int(round(possible_sales)),
            "Potential Expiry Units": int(round(expiry_risk)),
            "Status": status
        }

    return expiry_results