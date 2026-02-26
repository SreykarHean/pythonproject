from recommender import give_recommendation, summarize_competitors
import pandas as pd

# Pre-stored competitor datasets by industry
industries = {
    "coffee": "sample_data/compet_coffee.csv",
    "skincare": "sample_data/compet_skincare.csv"
}

# Global variables
user_data = None
competitors_data = None

# Admin-configurable recommendation rules
recommendation_config = {
    "sales_threshold": 10,   # default: competitor must be 10% higher
    "strategy": "marketing"  # default strategy
}

def choose_industry():
    print("\n--- Choose Industry ---")
    for i, ind in enumerate(industries.keys(), start=1):
        print(f"{i}. {ind.capitalize()}")
    print(f"{len(industries)+1}. Exit")

    choice = input("Enter choice: ")
    try:
        choice = int(choice)
        if 1 <= choice <= len(industries):
            industry = list(industries.keys())[choice-1]
            competitor_file = industries[industry]
            print(f"✅ Industry selected: {industry}")
            return competitor_file
        else:
            return None
    except ValueError:
        print("Invalid choice.")
        return None

def configure_rules():
    global recommendation_config
    print("\n--- Configure Recommendation Rules ---")
    try:
        threshold = int(input("Enter competitor sales threshold (% higher): "))
        strategy = input("Choose strategy (marketing/pricing): ").strip().lower()
        if strategy not in ["marketing", "pricing"]:
            print("⚠️ Invalid strategy. Defaulting to 'marketing'.")
            strategy = "marketing"
        recommendation_config["sales_threshold"] = threshold
        recommendation_config["strategy"] = strategy
        print(f"✅ Rules updated: threshold={threshold}%, strategy={strategy}")
    except ValueError:
        print("⚠️ Invalid input. Threshold must be a number.")

def view_rules():
    print("\n--- Current Recommendation Rules ---")
    print(f"Sales threshold: {recommendation_config['sales_threshold']}%")
    print(f"Strategy: {recommendation_config['strategy']}")

def manage_users():
    print("\n--- Manage Users ---")
    print("Currently, auth.py hardcodes admin and treats everyone else as user.")
    print("Future expansion could allow adding/removing accounts here.")

def analyze_multiple_competitors():
    global user_data, competitors_data
    if user_data is None or competitors_data is None:
        print("⚠️ Product or industry data not loaded yet.")
        return

    all_recs = []
    for comp in competitors_data:
        recs = give_recommendation(user_data, comp, recommendation_config)
        print(f"\n--- Recommendations vs {comp.get('product','Competitor')} ---")
        for r in recs:
            print("-", r)
        for r in recs:
            all_recs.append({"competitor": comp.get("product",""), "recommendation": r})

    # Export all recommendations
    pd.DataFrame(all_recs).to_csv("multi_competitor_recommendations.csv", index=False)
    print("✅ All recommendations exported to multi_competitor_recommendations.csv")

    # Show summary overview
    summary = summarize_competitors(user_data, competitors_data, recommendation_config)
    print("\n--- Industry Summary ---")
    print("\n".join(summary))

def console_menu(role="user"):
    global user_data, competitors_data

    # Step 1: Industry selection
    competitor_file = choose_industry()
    if competitor_file is None:
        print("Exiting...")
        return
    try:
        competitors_data = pd.read_csv(competitor_file).to_dict(orient="records")
        print(f"✅ Competitor dataset loaded from {competitor_file}")
    except Exception as e:
        print("Error loading competitor dataset:", e)
        return

    while True:
        print("\n--- Menu ---")
        print("1. Load Your Product Data (CSV)")
        print("2. View Recommendations (vs all competitors)")
        print("3. Export Recommendations (vs all competitors)")
        if role == "admin":
            print("4. Manage Users")
            print("5. Configure Recommendation Rules")
            print("6. View Current Rules")
            print("7. Analyze Multiple Competitors (with summary)")
            print("8. Exit")
        else:
            print("4. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            filename = input("Enter your product CSV filename (e.g., sample_data/user.csv): ")
            try:
                user_data = pd.read_csv(filename).iloc[0].to_dict()
                print("✅ Product data loaded.")
            except Exception as e:
                print("Error loading product file:", e)

        elif choice == "2":
            if user_data is None:
                print("⚠️ Product data not loaded yet (choice 1).")
            else:
                print("\n--- Consolidated Recommendations ---")
                for comp in competitors_data:
                    recs = give_recommendation(user_data, comp, recommendation_config)
                    print(f"\nAgainst {comp.get('product','Competitor')}:")
                    for r in recs:
                        print("-", r)

        elif choice == "3":
            if user_data is None:
                print("⚠️ Product data not loaded yet (choice 1).")
            else:
                all_recs = []
                for comp in competitors_data:
                    recs = give_recommendation(user_data, comp, recommendation_config)
                    for r in recs:
                        all_recs.append({"competitor": comp.get("product",""), "recommendation": r})
                pd.DataFrame(all_recs).to_csv("recommendations.csv", index=False)
                print("✅ Consolidated recommendations exported to recommendations.csv")

        elif role == "admin" and choice == "4":
            manage_users()

        elif role == "admin" and choice == "5":
            configure_rules()

        elif role == "admin" and choice == "6":
            view_rules()

        elif role == "admin" and choice == "7":
            analyze_multiple_competitors()

        elif (role == "admin" and choice == "8") or (role != "admin" and choice == "4"):
            print("Exiting...")
            break

        else:
            print("Invalid choice. Try again.")
