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
        print("  1. Select Industry")
        print("  2. Compare Products")
        print("  3. Logout")
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

    # def _select_industry(self)

    # def _view_brand_products(): # Nysa 
      

    # ── Compare Products  SREYKAR──────────────────────────────────────────────────────

    # def _compare_products(self):

    # ── Sessions  Management Kimheng──────────────────────────────────────────────────────────────
    #
    def _user_session(self, username):
        while True:
            self._user_menu(username)
            choice = input("  Choose option: ").strip()

            if choice == "1":
                self._select_industry()
            elif choice == "2":
                self._compare_products()
            elif choice == "3":
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