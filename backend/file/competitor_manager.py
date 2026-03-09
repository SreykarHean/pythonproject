import pandas as pd
import os

DATASET_PATH    = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../Dataset/all_industries_organized.csv")
COMPETITOR_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../Dataset/competitors.csv")
IMPORT_FOLDER   = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../Dataset/imports")

COMPETITOR_COLUMNS = ['name', 'industry', 'category', 'price', 'user_rating', 'user_reviews', 'price_band', 'rating_tier']


class CompetitorManager:

    def __init__(self):
        self._df = self._load_competitors()

    # ── Internal helpers ──────────────────────────────────────────────────────

    def _load_competitors(self):
        if os.path.exists(COMPETITOR_PATH):
            return pd.read_csv(COMPETITOR_PATH)
        return pd.DataFrame(columns=COMPETITOR_COLUMNS)

    def _save_competitors(self):
        self._df.to_csv(COMPETITOR_PATH, index=False)

    def _assign_price_band(self, price):
        try:
            price = float(price)
        except (ValueError, TypeError):
            return 'Unknown'
        if price <= 25:   return 'Budget ($0-25)'
        if price <= 50:   return 'Mid ($26-50)'
        if price <= 100:  return 'Premium ($51-100)'
        if price <= 250:  return 'Luxury ($101-250)'
        return 'Ultra ($250+)'

    def _assign_rating_tier(self, rating):
        try:
            rating = float(rating)
        except (ValueError, TypeError):
            return 'Unknown'
        if rating <= 2.9: return 'Low (1-2.9)'
        if rating <= 3.9: return 'Average (3-3.9)'
        if rating <= 4.4: return 'Good (4-4.4)'
        return 'Top Rated (4.5-5)'

    def _build_row(self, name, industry, category, price, rating, reviews):
        return {
            'name':         name.strip(),
            'industry':     industry.strip(),
            'category':     category.strip(),
            'price':        float(price),
            'user_rating':  float(rating),
            'user_reviews': int(reviews),
            'price_band':   self._assign_price_band(price),
            'rating_tier':  self._assign_rating_tier(rating),
        }

    # ── List CSV files in imports folder ──────────────────────────────────────

    def _get_csv_file(self):
        os.makedirs(IMPORT_FOLDER, exist_ok=True)
        folder_files = [f for f in os.listdir(IMPORT_FOLDER) if f.endswith('.csv')]

        print("\n  How would you like to provide the CSV file?")
        print("  1. Type / paste file path")
        print("  2. Choose from imports folder")
        choice = input("  Choose option: ").strip()

        if choice == "1":
            path = input("\n  Enter CSV file path: ").strip().strip('"').strip("'")
            if not os.path.exists(path):
                print(f"  ✗ File not found: {path}")
                return None, None
            return path, os.path.basename(path)

        elif choice == "2":
            if not folder_files:
                print(f"\n  No CSV files found in imports folder.")
                print(f"  ➜  {IMPORT_FOLDER}")
                return None, None
            print(f"\n  CSV files in imports folder:")
            for i, f in enumerate(folder_files, 1):
                size = os.path.getsize(os.path.join(IMPORT_FOLDER, f))
                print(f"    {i}. {f}  ({size/1024:.1f} KB)")
            print(f"    0. Cancel")
            while True:
                val = input("\n  Select file: ").strip()
                if val == "0":
                    return None, None
                if val.isdigit() and 1 <= int(val) <= len(folder_files):
                    filename = folder_files[int(val) - 1]
                    return os.path.join(IMPORT_FOLDER, filename), filename
                print("  Invalid option.")
        else:
            print("  Invalid option.")
            return None, None
        
    # CRUD Operation

    # ── Add competitor ────────────────────────────────────────────────────────
    #NYSA.S PART
    def add_competitor(self):
        print("\nHow would you like to add a competitor?")
        print("  1. Manual input")
        print("  2. Import from CSV file")
        choice = input("Choose option: ").strip()

        if(choice == "1"):
            self._add_manual()
        elif(choice == "2"):
            self._add_from_csv()
        else:
            print("Invalid option.")

    # NYSA.S  PART
    def _add_manual(self):
        print("\n ==== Add New Competetor (Manaul) ====")

        try:
            name = input("Product Name: ")
            industry = input("Industry: ")
            category = input("Category: ")
            price = float(input("Price: "))
            rating = float(input("Rating: "))
            reviews = int(input("Reviews: "))

            new_row = self._build_row(name, industry, category, price, rating, reviews)

            # Add to list and Save
            self._df = pd.concat([self._df, pd.DataFrame([new_row])], ignore_index=True)
            self._save_competitors()
            print(f"Product: {name} added!")

        except ValueError:
            print("Error: Price, Rating, and Review must be numeric.")

    def _add_from_csv(self):
        path, filename = self._get_csv_file()
        if (not path): return
        try:
            new_data = pd.read_csv(path)
            required = ['name', 'industry', 'category', 'price', 'user_rating', 'user_reviews']
            
            if (all(col in new_data.columns for col in required)):
                # Ensure price  rating tiers are calculated for the new data
                new_data['price_band'] = new_data['price'].apply(self._assign_price_band)
                new_data['rating_tier'] = new_data['user_rating'].apply(self._assign_rating_tier)
                
                self._df = pd.concat([self._df, new_data[COMPETITOR_COLUMNS]], ignore_index=True)
                self._save_competitors()
                print(f"Successfully imported {len(new_data)} records from {filename}")
            else:
                print(f"CSV missing required columns: {required}")
        except Exception as e:
            print(f"Error reading CSV: {e}")

    # ── Update competitor NYSA PART─────────────────────────────────────────────────────
    def update_competitor(self):
        print("\n==== Update Competitor ====")
        name = input("Enter the Product Name to update: ").strip()
        
        if(name in self._df['name'].values):
            print(f"Updating details for: {name}")
            new_price = input("Enter New Price (leave blank to keep current): ")
            new_rating = input("Enter New Rating (leave blank to keep current): ")
            
            # Find the row index for this product
            idx = self._df[self._df['name'] == name].index[0]
            
            if(new_price):
                self._df.at[idx, 'price'] = float(new_price)
                # Re-calculate the price band based on the new price
                self._df.at[idx, 'price_band'] = self._assign_price_band(new_price)
            
            if(new_rating):
                self._df.at[idx, 'user_rating'] = float(new_rating)
                # Re calculate the rating tier
                self._df.at[idx, 'rating_tier'] = self._assign_rating_tier(new_rating)
                
            self._save_competitors()
            print(f"product: {name} updated successfully.")
        else:
            print("Product not found.")
        
    # ── Delete competitor NYSA PART ─────────────────────────────────────────────────────
    def delete_competitor(self):
        print("\n==== Delete Competitor ====")
        name_to_delete = input(" Enter Product Name to remove: ").strip()
        # Check if the name exist
        if(name_to_delete in self._df['name'].values):
            # Keep only the rows that do NOT match the name
            self._df = self._df[self._df['name'] != name_to_delete]
            self._save_competitors() # Save the change to CSV
            print(f"Product: {name_to_delete} has been removed successfully.")
        else:
            print(f"Product: '{name_to_delete}' not found in the list.")

    # ── View competitors NYSA PART ──────────────────────────────────────────────────────

    def view_competitors(self):
        print("\n── Current Competitor List ──")
        if self._df.empty:
            print("The list is currently empty.")
        else:
            # Displaying specific columns 
            columns_to_show = ['name', 'industry', 'price', 'user_rating']
            print(self._df[columns_to_show].to_string(index = False))


     # ── Analytics SREYKAR YOU may design how ever you want with the menu─────────────────────────────────────────────────────────────

    def analytics(self):
        while True:
            print("\n  Analytics Menu")
            print("  ─"*18)
            print("  1. Compare with dataset")
            print("  2. Top rated competitors")
            print("  3. Price breakdown by industry")
            print("  4. Recommendation")
            print("  5. Back")
            choice = input("  Choose option: ").strip()

            if choice == "1":
                self._compare_with_dataset()
            elif choice == "2":
                self._top_rated()
            elif choice == "3":
                self._price_breakdown()
            elif choice == "4":
                self.recommend_products()
            elif choice == "5":
                break
            else:
                print("  Invalid option.")

    def _compare_with_dataset(self):
        if self._df.empty:
            print("No competitor data.")
            return

        dataset = pd.read_csv(DATASET_PATH)

        print("\nMarket Comparison")
        print("────────────────────")

        avg_comp_price = self._df['price'].mean()
        avg_market_price = dataset['price'].mean()

        avg_comp_rating = self._df['user_rating'].mean()
        avg_market_rating = dataset['user_rating'].mean()

        print(f"Competitor avg price: ${avg_comp_price:.2f}")
        print(f"Market avg price: ${avg_market_price:.2f}")

        print(f"\nCompetitor avg rating: {avg_comp_rating:.2f}")
        print(f"Market avg rating: {avg_market_rating:.2f}")

        if avg_comp_rating > avg_market_rating:
            print("\nCompetitors perform ABOVE market average")
        else:
            print("\nCompetitors perform BELOW market average")


    def _top_rated(self):
        if self._df.empty:
            print("No competitor data.")
            return

        top = self._df.sort_values(by="user_rating", ascending=False).head(10)

        print("\nTop Rated Competitors")
        print("────────────────────────")

        for _, row in top.iterrows():
            print(f"{row['name']} | ⭐️ {row['user_rating']} | ${row['price']}")
  
  
    def _price_breakdown(self):
        if self._df.empty:
            print("No competitor data.")
            return

        breakdown = self._df.groupby("industry")["price"].mean()

        print("\nAverage Price by Industry")
        print("────────────────────────")

        for industry, price in breakdown.items():
            print(f"{industry}: ${price:.2f}")

    #____________RECOMMENDATION SYSTEM_____SREYKAR

    def recommend_products(self):
        dataset = pd.read_csv(DATASET_PATH)

        print("\nRecommendation System")
        print("────────────────────")

        industry = input("Choose industry (Coffee/Shoes/Foods/Skincare): ").strip()

        filtered = dataset[dataset['source'].str.contains(industry, case=False, na=False)]

        if filtered.empty:
            print("No products found.")
            return

        # scoring formula
        filtered['score'] = (
            filtered['user_rating'] * 0.6 +
            (filtered['user_reviews'] / filtered['user_reviews'].max()) * 0.3 +
            (1 / filtered['price']) * 0.1
        )

        top = filtered.sort_values(by="score", ascending=False).head(5)

        print("\nRecommended Products")
        print("────────────────────")

        for _, row in top.iterrows():
            print(
                f"{row['product_name']} | {row['brand']} | "
                f"${row['price']} | ⭐️{row['user_rating']}"
            )
