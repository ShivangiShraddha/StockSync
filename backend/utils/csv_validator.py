import pandas as pd
def validate_and_clean_csv(file_path):
    
    required_columns = [
        "date",
        "product_name",
        "quantity_sold",
        "current_stock"
    ]
    
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        return None, f"Error reading file: {e}"
    
    # Check required columns
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        return None, f"Missing required columns: {missing_cols}"
    
    # Convert date
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    if df["date"].isnull().any():
        return None, "Invalid date format detected."
    
    # Convert numeric columns
    df["quantity_sold"] = pd.to_numeric(df["quantity_sold"], errors="coerce")
    df["current_stock"] = pd.to_numeric(df["current_stock"], errors="coerce")
    
    if df[["quantity_sold", "current_stock"]].isnull().any().any():
        return None, "Invalid numeric values detected."
    
    # Minimum data check per product
    for product in df["product_name"].unique():
        if len(df[df["product_name"] == product]) < 45:
            return None, f"Not enough data for product: {product} (Minimum 45 days required)"
    
    return df, "File validated successfully"