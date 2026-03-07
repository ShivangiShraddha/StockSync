def calculate_revenue(df, forecast_results):

    revenue_results = {}

    # Example price mapping (can later come from DB)
    price_catalog = {
        "Rice": 40,
        "Oil": 120,
        "Sugar": 45,
        "Milk": 50,
        "Soap": 30
    }

    forecast_days = 30

    products = forecast_results.keys()

    for product in products:

        predicted_daily_demand = forecast_results[product]["Predicted Daily Demand"]

        price = price_catalog.get(product, 50)

        predicted_sales = predicted_daily_demand * forecast_days

        predicted_revenue = predicted_sales * price

        revenue_results[product] = {
            "Price": price,
            "Forecast Days": forecast_days,
            "Predicted Sales": int(round(predicted_sales)),
            "Predicted Revenue": int(round(predicted_revenue))
        }

    return revenue_results