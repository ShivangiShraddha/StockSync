from flask import Flask, request, jsonify
import pandas as pd
import os

from utils.csv_validator import validate_and_clean_csv
from services.demand_forecast import forecast_demand
from services.inventory_service import calculate_inventory
from services.revenue_service import calculate_revenue
from services.expiry_service import detect_expiry

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route("/")
def home():
    return "Business Analytics SaaS Backend Running"


@app.route("/upload", methods=["POST"])
def upload_file():

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # ---------- CSV VALIDATION ----------
    df, message = validate_and_clean_csv(file_path)

    if df is None:
        return jsonify({"error": message}), 400

    # ---------- ML DEMAND FORECAST ----------
    forecast_results = forecast_demand(df)

    # ---------- INVENTORY ANALYSIS ----------
    inventory_results = calculate_inventory(df, forecast_results)

    # ---------- REVENUE PREDICTION ----------
    revenue_results = calculate_revenue(df, forecast_results)

    # ---------- EXPIRY DETECTION ----------
    expiry_results = detect_expiry(df, forecast_results)

    # ---------- FINAL RESPONSE ----------
    response = {
        "Demand Forecast": forecast_results,
        "Inventory Analysis": inventory_results,
        "Revenue Forecast": revenue_results,
        "Expiry Risk": expiry_results
    }

    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)