import pandas as pd

def load_competitors(industry, use_api=False):
    """
    Load competitor data for a given industry.
    If use_api=True, return mock API data (simulated).
    Otherwise, fall back to CSV.
    """

    # Define CSV fallback files
    csv_files = {
        "coffee": "sample_data/compet_coffee.csv",
        "skincare": "sample_data/compet_skincare.csv"
    }

    try:
        if use_api:
            # Simulated API response for testing
            if industry == "coffee":
                data = mock_coffee_api_response()
            elif industry == "skincare":
                data = mock_skincare_api_response()
            else:
                raise ValueError("No mock API data defined for this industry.")
            print(f"✅ Competitor data loaded from MOCK API ({industry})")
            return normalize_api_data(data)
        else:
            filename = csv_files.get(industry)
            if not filename:
                raise ValueError("No CSV file defined for this industry.")
            data = pd.read_csv(filename).to_dict(orient="records")
            print(f"✅ Competitor data loaded from CSV ({industry})")
            return data
    except Exception as e:
        print("⚠️ Error loading competitor data:", e)
        return []

def normalize_api_data(data):
    """
    Normalize API response into the format:
    { product, price, sales, rating }
    """
    competitors = []
    for item in data:
        competitors.append({
            "product": item.get("product"),
            "price": item.get("price"),
            "sales": item.get("sales"),
            "rating": item.get("rating")
        })
    return competitors

def mock_coffee_api_response():
    """
    Simulated API response for coffee products (like Amazon would return).
    """
    return [
        {"product": "Starbucks Pike Place Roast", "price": 12.99, "sales": 1200, "rating": 4.6},
        {"product": "Lavazza Espresso Italiano", "price": 9.49, "sales": 950, "rating": 4.4},
        {"product": "Peet's Major Dickason's Blend", "price": 14.99, "sales": 800, "rating": 4.7},
        {"product": "Folgers Classic Roast", "price": 8.99, "sales": 1500, "rating": 4.3},
        {"product": "Death Wish Coffee", "price": 19.99, "sales": 600, "rating": 4.5}
    ]

def mock_skincare_api_response():
    """
    Simulated API response for skincare products (example).
    """
    return [
        {"product": "Skin1004 Centella Ampoule", "price": 18.99, "sales": 500, "rating": 4.6},
        {"product": "Innisfree Green Tea Serum", "price": 22.50, "sales": 400, "rating": 4.4},
        {"product": "Cosrx Snail Mucin Essence", "price": 25.00, "sales": 700, "rating": 4.7}
    ]
