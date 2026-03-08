# recommender.py

def give_recommendation(user_data, competitor_data, config):
    recs = []
    try:
        # Extract values from CSV dictionaries
        user_product = user_data.get("product", "Your Product")
        user_price = float(user_data.get("price", 0))
        user_sales = int(user_data.get("sales", 0))
        user_rating = float(user_data.get("rating", 0))

        competitor_product = competitor_data.get("product", "Competitor Product")
        competitor_price = float(competitor_data.get("price", 0))
        competitor_sales = int(competitor_data.get("sales", 0))
        competitor_rating = float(competitor_data.get("rating", 0))

        # Use admin-configured rules
        threshold = config.get("sales_threshold", 10)
        strategy = config.get("strategy", "marketing")

        # Sales comparison
        if competitor_sales > user_sales * (1 + threshold/100):
            if strategy == "marketing":
                recs.append(f"{competitor_product} has significantly higher sales. Increase marketing efforts for {user_product}.")
            elif strategy == "pricing":
                recs.append(f"{competitor_product} has significantly higher sales. Consider adjusting {user_product}'s pricing strategy.")
        else:
            recs.append(f"{user_product} sales are competitive compared to {competitor_product}.")

        # Price comparison
        if competitor_price < user_price:
            recs.append(f"{competitor_product} is cheaper. Explore cost reduction or highlight premium value of {user_product}.")
        elif competitor_price > user_price:
            recs.append(f"{user_product} is more affordable than {competitor_product}. Emphasize value in marketing.")

        # Rating comparison
        if competitor_rating > user_rating:
            recs.append(f"{competitor_product} has a higher rating ({competitor_rating}). Focus on improving customer satisfaction for {user_product}.")
        elif competitor_rating < user_rating:
            recs.append(f"{user_product} has a better rating ({user_rating}). Highlight quality advantage over {competitor_product}.")

    except Exception as e:
        recs.append(f"Error generating recommendation: {e}")

    return recs


def summarize_competitors(user_data, competitors, config):
    """
    Admin-only: Summarize multiple competitors with rankings.
    """
    summary = []
    try:
        # Sort competitors by sales (descending)
        competitors_sorted = sorted(competitors, key=lambda c: int(c.get("sales", 0)), reverse=True)

        summary.append("\n--- Competitor Rankings by Sales ---")
        for idx, comp in enumerate(competitors_sorted, start=1):
            summary.append(f"{idx}. {comp.get('product','Unknown')} - Sales: {comp.get('sales','N/A')}")

        # Best-rated competitor
        best_rated = max(competitors, key=lambda c: float(c.get("rating", 0)))
        summary.append(f"\nHighest-rated competitor: {best_rated.get('product')} ({best_rated.get('rating')})")

        # Cheapest competitor
        cheapest = min(competitors, key=lambda c: float(c.get("price", 0)))
        summary.append(f"Lowest-priced competitor: {cheapest.get('product')} (${cheapest.get('price')})")

    except Exception as e:
        summary.append(f"Error summarizing competitors: {e}")

    return summary
