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

    # ── Add competitor ────────────────────────────────────────────────────────
    #NYSA PA
    def add_competitor(self):
        print("\nHow would you like to add a competitor?")
        print("  1. Manual input")
        print("  2. Import from CSV file")
        choice = input("  Choose option: ").strip()

        if choice == "1":
            self._add_manual()
        elif choice == "2":
            self._add_from_csv()
        else:
            print("  Invalid option.")
    #NYSA PART
    # def _add_manual(self):
    # def _add_from_csv(self):
   
    # ── Update competitor NYSA PART─────────────────────────────────────────────────────

    # def update_competitor(self):
        
    # ── Delete competitor NYSA PART ─────────────────────────────────────────────────────

    # def delete_competitor(self):
      
    # ── View competitors NYSA PART ──────────────────────────────────────────────────────

    # def view_competitors(self): 


    # ── Analytics SREYKAR YOU may design how ever you want with the menu─────────────────────────────────────────────────────────────

    def analytics(self):
        while True:
            print("\n  Analytics Menu")
            print("  ─"*18)
            print("  1. Compare with dataset")
            print("  2. Top rated competitors")
            print("  3. Price breakdown by industry")
            print("  4. .............")
            print("  5. Back")
            choice = input("  Choose option: ").strip()

            if choice == "1":
                self._compare_with_dataset()
            elif choice == "2":
                self._top_rated()
            elif choice == "3":
                self._price_breakdown()
            elif choice == "5":
                break
            else:
                print("  Invalid option.")

    # def _compare_with_dataset(self):
    # def _top_rated(self):
    # def _price_breakdown(self):

    #____________RECOMMENDATION SYSTEM_____SREYKAR
