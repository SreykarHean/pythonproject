import os
import json
from competitor_manager import CompetitorManager
from data_organizer import DataOrganizer

USERS_PATH  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "users.json")
DATASET_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../Dataset/all_industries_organized.csv")


class AuthSystem:

    def __init__(self):
        self._users             = self._load_users()
        self.competitor_manager = CompetitorManager()
        self.data_organizer     = DataOrganizer()

    # ── User persistence ──────────────────────────────────────────────────────

    def _load_users(self):
        if os.path.exists(USERS_PATH):
            with open(USERS_PATH, 'r') as f:
                return json.load(f)
        return {
            "lykimheng": "IDTB110235@",
            "ly":        "IDTB110235#"
        }

    def _save_users(self):
        with open(USERS_PATH, 'w') as f:
            json.dump(self._users, f, indent=2)

    # ── Menus ─────────────────────────────────────────────────────────────────

    def _display_menu(self):
        print("\n" + "═"*35)
        print("       COMPETITOR TRACKER")
        print("═"*35)
        print("  1. Register")
        print("  2. Login")
        print("  3. Forgot Password")
        print("  4. Exit")
        print("─"*35)

    def _user_menu(self, username):
        print(f"\n  Welcome, {username}!")
        print("─"*35)
        print("  1. Enter My Product")
        print("  2. Select Industry")
        print("  3. Compare Products")
        print("  4. Recommendation")
        print("  5. Logout")
        print("─"*35)

    def _admin_menu(self):
        print("\n" + "═"*35)
        print("         ADMIN PANEL")
        print("═"*35)
        print("  1. Add Competitor")
        print("  2. Update Competitor")
        print("  3. Delete Competitor")
        print("  4. Organize Data")
        print("  5. Select Industry")
        print("  6. View Competitors")
        print("  7. Analytics")
        print("  8. Logout")
        print("─"*35)

    # ── Password validation ───────────────────────────────────────────────────

    def _validate_password(self, password):
        special = "!@#$%&*()"
        checks = [
            (len(password) >= 8,                          "at least 8 characters"),
            (any(c.isupper() for c in password),          "an uppercase letter"),
            (any(c.islower() for c in password),          "a lowercase letter"),
            (any(c.isdigit() for c in password),          "a digit"),
            (any(c in special for c in password),         f"a special character ({special})"),
        ]
        for passed, requirement in checks:
            if not passed:
                print(f"  ✗ Password must contain {requirement}.")
                return False
        return True

    # ── Auth actions ──────────────────────────────────────────────────────────

    def _register(self):
        print("\n── Register ──")
        while True:
            username = input("  Username: ").strip()
            if not username:
                print("  Username cannot be empty.")
            elif username in self._users:
                print("  Username already exists.")
            else:
                break

        while True:
            password = input("  Password: ").strip()
            if self._validate_password(password):
                break

        self._users[username] = password
        self._save_users()
        print(f"\n  ✓ Registration successful! Welcome, {username}.")

    def _is_admin(self, username, password):
        return username == "Kimheng" and password == "Kimheng123!"

    def _login(self):
        print("\n── Login ──")
        username = input("  Username: ").strip()
        password = input("  Password: ").strip()

        if self._is_admin(username, password):
            print("\n  ✓ Admin login successful!")
            self._admin_session()
            return

        if username in self._users and self._users[username] == password:
            print(f"\n  ✓ Login successful!")
            self._user_session(username)
        else:
            print("\n  ✗ Invalid username or password.")

    def _forgot_password(self):
        print("\n── Forgot Password ──")
        username = input("  Enter your username: ").strip()
        if username in self._users:
            print(f"\n  Your password is: {self._users[username]}")
        else:
            print("\n  ✗ Username not found.")

    # ── Select Industry  NYSA PART  with Industry filtering Logic───────────────────────────────────────────────────────

   # ── Select Industry NYSA PART ───────────────────────────────────────────────────────

    def _select_industry(self):
        """ Loads the organized dataset, displays unique industries, and allows the user to pick one to view."""
        if(not os.path.exists(DATASET_PATH)):
            print("Error: Organized dataset not found at path.")
            return

        import pandas as pd
        # Load the dataset to get the most current industry list
        df = pd.read_csv(DATASET_PATH) # read CSV file into dataframe
        
        # get unique industries and sort them for the menu
        if ('industry' in df.columns):
            industries = (
                df['industry']
                .dropna()          # remove NaN values
                .astype(str)       # convert everything to string
                .str.strip()       # remove extra spaces
                .unique().tolist()
            )
            industries.sort()      # sort after cleaning
        else:
            print(f"Error: Column 'industry' not found. Available columns: {df.columns.tolist()}")
            return

        print("\n==== Select Industry ====")
        for i, ind in enumerate(industries, 1): 
            print(f"{i}.{ind}")
        print(f"{len(industries) + 1}. Back")

        choice = input("\n  Choose industry number: ").strip()

        try:
            choice_idx = int(choice) - 1
            if(0 <= choice_idx < len(industries)):
                selected = industries[choice_idx]
                self._view_brand_products(df, selected)
            elif(choice_idx == len(industries)):
                return
            else:
                print("  Invalid selection.")

        except ValueError:
            print("  Please enter a valid number.")

    def _view_brand_products(self, df, industry_name):
        """Displays products belonging to a specific industry."""

        # Filter the dataframe for the selected industry
        filtered_df = df[df['industry'] == industry_name]

        print(f"\n==== {industry_name.upper()} Products ====")
        
        if(filtered_df.empty):
            print(f"  No products found for the {industry_name} industry.")
        else:
            # Displaying specific columns for clarity
            cols_to_show = ['product_name', 'brand', 'price', 'user_rating']
            
            # Use .head(15) to prevent terminal flooding
            print(filtered_df[cols_to_show].head(15).to_string(index = False))
            
            total_count = len(filtered_df)
            if(total_count > 15):
                print(f"\n  ...... and {total_count - 15} more products.")
        
        input("\n  Press Enter to return.........")

     # ── Enter My Product ──────────────────────────────────────────────────────

    def _enter_my_product(self):
        print("\n── Enter My Product ──")
        try:
            name     = input("  Product Name: ").strip()
            industry = input("  Industry (Coffee/Foods/Shoes/Skincare): ").strip()
            category = input("  Category: ").strip()
            price    = float(input("  Price: $").strip())
            rating   = float(input("  Your Rating (1-5): ").strip())
            reviews  = int(input("  Number of Reviews: ").strip())

            self._my_product = {
                'product_name': name,
                'industry':     industry,
                'category':     category,
                'price':        price,
                'user_rating':  rating,
                'user_reviews': reviews,
            }
            print(f"\n  ✓ Product '{name}' saved! You can now Compare or get a Recommendation.")

        except ValueError:
            print("  ✗ Price, Rating, and Reviews must be numbers.")

     # ── Compare Products  SREYKAR──────────────────────────────────────────────────────

    def _compare_products(self):

        import pandas as pd

        if not hasattr(self, '_my_product') or not self._my_product:
            print("\n  ✗ Please enter your product first (Option 1).")
            return

        if not os.path.exists(DATASET_PATH):
            print("Dataset not found.")
            return

        df = pd.read_csv(DATASET_PATH)

        my = self._my_product
        industry = my['industry']

        filtered = df[df['industry'].str.contains(industry, case=False, na=False)]

        if filtered.empty:
            print(f"\n  No competitor data found for industry: {industry}")
            return

        avg_price  = filtered['price'].mean()
        avg_rating = filtered['user_rating'].mean()

        print(f"\n── Comparison: {my['product_name']} vs {industry} Market ──")
        print("─"*50)
        print(f"{'':25} {'Your Product':>12}  {'Market Avg':>10}")
        print(f"  {'Price':<23} ${my['price']:>11.2f}  ${avg_price:>9.2f}")
        print(f"  {'Rating':<23} {my['user_rating']:>12.2f}  {avg_rating:>10.2f}")
        print("─"*50)

        if my['price'] < avg_price:
            print(f"  ✓ Your price is LOWER than market average by ${avg_price - my['price']:.2f}")
        else:
            print(f"  ✗ Your price is HIGHER than market average by ${my['price'] - avg_price:.2f}")

        if my['user_rating'] >= avg_rating:
            print(f"  ✓ Your rating is ABOVE market average by {my['user_rating'] - avg_rating:.2f}")
        else:
            print(f"  ✗ Your rating is BELOW market average by {avg_rating - my['user_rating']:.2f}")

        print("\n  Top 5 Competitors in your industry:")
        print("  ─"*25)
        top = filtered.sort_values('user_rating', ascending=False).head(5)
        for _, row in top.iterrows():
            print(f"  {row['product_name']} | {row['brand']} | ${row['price']:.2f} | {row['user_rating']:.2f}")


    # ── Sessions  Management Kimheng──────────────────────────────────────────────────────────────
    #
    def _user_recommendation(self):
        import pandas as pd

        if not hasattr(self, '_my_product') or not self._my_product:
            print("\n  ✗ Please enter your product first (Option 1).")
            return

        if not os.path.exists(DATASET_PATH):
            print("  Dataset not found.")
            return

        df = pd.read_csv(DATASET_PATH)
        my       = self._my_product
        industry = my['industry']

        filtered = df[df['industry'].str.contains(industry, case=False, na=False)].copy()
        filtered = filtered.dropna(subset=['price', 'user_rating'])

        if filtered.empty:
            print(f"  No products found for '{industry}'")
            return

        avg_price   = filtered['price'].mean()
        avg_rating  = filtered['user_rating'].mean()
        avg_reviews = filtered['user_reviews'].mean()
        top_rating  = filtered['user_rating'].max()
        top_price   = filtered.sort_values('user_rating', ascending=False).iloc[0]['price']

        print(f"\n  ── Recommendation for '{my['product_name']}' ──")
        print("  " + "─"*45)

        tips = []

        # Price feedback
        price_diff = my['price'] - avg_price
        if price_diff > avg_price * 0.3:
            tips.append(f"Price: Your price (${my['price']:.2f}) is much HIGHER than the market average (${avg_price:.2f}).\n"
                        f"→ Consider lowering your price to attract more customers.")
        elif price_diff > 0:
            tips.append(f"Price: Your price (${my['price']:.2f}) is slightly above market average (${avg_price:.2f}).\n"
                        f"→ You may want to justify this with better quality or branding.")
        else:
            tips.append(f"Price: Your price (${my['price']:.2f}) is competitive vs market average (${avg_price:.2f}).\n"
                        f"→ Good! Keep your price at this range to stay competitive.")

        # Rating feedback
        rating_diff = avg_rating - my['user_rating']
        if my['user_rating'] >= top_rating * 0.95:
            tips.append(f"Rating: Excellent! Your rating ({my['user_rating']:.2f}) is among the top in the market.\n"
                        f"→ Keep maintaining your product quality.")
        elif rating_diff > 0.5:
            tips.append(f"Rating: Your rating ({my['user_rating']:.2f}) is BELOW market average ({avg_rating:.2f}).\n"
                        f"→ Focus on improving product quality and customer experience.\n"
                        f"→ Top competitors reach ratings up to {top_rating:.2f}.")
        elif rating_diff > 0:
            tips.append(f"Rating: Your rating ({my['user_rating']:.2f}) is close to market average ({avg_rating:.2f}).\n"
                        f"→ Small improvements in quality could push you above average.")
        else:
            tips.append(f"Rating: Your rating ({my['user_rating']:.2f}) is ABOVE market average ({avg_rating:.2f}).\n"
                        f"→ Great! Use this as a selling point in your marketing.")

        # Reviews feedback
        if my['user_reviews'] < avg_reviews * 0.5:
            tips.append(f"Reviews: You only have {my['user_reviews']} reviews vs market average of {avg_reviews:.0f}.\n"
                        f"→ Encourage customers to leave reviews to build trust and visibility.")
        elif my['user_reviews'] >= avg_reviews:
            tips.append(f"Reviews: Good review count ({my['user_reviews']}) vs market average ({avg_reviews:.0f}).\n"
                        f"→ Keep engaging customers for more feedback.")

        # Overall summary
        print()
        for tip in tips:
            print(tip)

        print()
        print("  ── Top 3 competitors to learn from ──")
        print("  " + "─"*45)
        top3 = filtered.sort_values('user_rating', ascending=False).head(3)
        for _, row in top3.iterrows():
            print(f"  {row['product_name']} | {row['brand']} | ${row['price']:.2f} | {row['user_rating']:.2f}")

        input("\n  Press Enter to return.........")

    def _user_session(self, username):
        self._my_product = None
        while True:
            self._user_menu(username)
            choice = input("  Choose option: ").strip()

            if choice == "1":
                self._enter_my_product()
            elif choice == "2":
                self._select_industry()
            elif choice == "3":
                self._compare_products()
            elif choice == "4":
                self._user_recommendation()
            elif choice == "5":
                print(f"\n  Goodbye, {username}!")
                break
            else:
                print("  Invalid option.")

    def _admin_session(self):
        while True:
            self._admin_menu()
            choice = input("  Choose option: ").strip()

            if choice == "1":
                self.competitor_manager.add_competitor()
            elif choice == "2":
                self.competitor_manager.update_competitor()
            elif choice == "3":
                self.competitor_manager.delete_competitor()
            elif choice == "4":
                self.data_organizer.import_and_organize()
            elif choice == "5":
                self._select_industry()
            elif choice == "6":
                self.competitor_manager.view_competitors()
            elif choice == "7":
                self.competitor_manager.analytics()
            elif choice == "8":
                print("\n  Admin logged out.")
                break
            else:
                print("  Invalid option.")

    # ── Main loop ─────────────────────────────────────────────────────────────

    def run(self):
        while True:
            self._display_menu()
            choice = input("  Choose option: ").strip()

            if choice == "1":
                self._register()
            elif choice == "2":
                self._login()
            elif choice == "3":
                self._forgot_password()
            elif choice == "4":
                print("\n  Program exited. Goodbye!\n")
                break
            else:
                print("  Invalid option.")