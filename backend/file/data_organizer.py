import pandas as pd
import os

DATASET_PATH  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../Dataset/all_industries_organized.csv")
IMPORT_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../Dataset/imports")
MAX_ROWS      = 300

INDUSTRIES = ['Shoes', 'Foods', 'Coffee', 'Skincare']

FIELD_PATTERNS = {
    'product_name': ['product_name', 'name', 'title', 'product', 'item', 'menu_item_name', 'beverage', 'product_title'],
    'brand':        ['brand', 'brand_name', 'manufacturer', 'maker', 'cuisine_type', 'restaurant_type', 'beverage_category'],
    'price':        ['price', 'price_usd', 'actual_selling_price', 'sale_price', 'cost', 'calories'],
    'user_rating':  ['rating', 'avg_rating', 'user_rating', 'stars', 'score', 'quantity_sold'],
    'user_reviews': ['reviews', 'review_count', 'user_reviews', 'num_reviews', 'ratings_count'],
    'category':     ['category', 'primary_category', 'sub_title', 'type', 'genre', 'beverage_prep', 'color'],
}


def _auto_map(columns):
    cols_lower = {c.lower(): c for c in columns}
    mapping = {}
    for field, patterns in FIELD_PATTERNS.items():
        for pattern in patterns:
            if pattern.lower() in cols_lower:
                mapping[field] = cols_lower[pattern.lower()]
                break
        if field not in mapping:
            mapping[field] = None
    return mapping


def _assign_price_band(price):
    try:
        p = float(price)
    except (ValueError, TypeError):
        return None
    if p <= 25:   return 'Budget ($0-25)'
    if p <= 50:   return 'Mid ($26-50)'
    if p <= 100:  return 'Premium ($51-100)'
    if p <= 250:  return 'Luxury ($101-250)'
    return 'Ultra ($250+)'


def _assign_rating_tier(rating):
    try:
        r = float(rating)
    except (ValueError, TypeError):
        return None
    if r <= 2.9:  return 'Low (1-2.9)'
    if r <= 3.9:  return 'Average (3-3.9)'
    if r <= 4.4:  return 'Good (4-4.4)'
    return 'Top Rated (4.5-5)'


class DataOrganizer:

    # ── Get CSV file from user input or imports folder ────────────────────────

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
                if val == '0':
                    return None, None
                if val.isdigit() and 1 <= int(val) <= len(folder_files):
                    filename = folder_files[int(val) - 1]
                    return os.path.join(IMPORT_FOLDER, filename), filename
                print("  Invalid option.")
        else:
            print("  Invalid option.")
            return None, None

    # ── Show auto-detected mapping & let admin confirm/fix ────────────────────

    def _confirm_mapping(self, df, mapping):
        print(f"\n  Auto-detected column mapping:")
        print(f"  {'Field':<15} {'Mapped To':<30} {'Sample Value'}")
        print(f"  {'─'*65}")
        for field, col in mapping.items():
            if col:
                sample = str(df[col].dropna().iloc[0]) if not df[col].dropna().empty else 'N/A'
                sample = sample[:25] + '...' if len(sample) > 25 else sample
                print(f"  {field:<15} {col:<30} {sample}")
            else:
                print(f"  {field:<15} {'(not found)':<30} —")

        fix = input("\n  Is this mapping correct? (y/n): ").strip().lower()
        if fix == 'n':
            print(f"\n  Available columns:")
            for i, col in enumerate(df.columns, 1):
                print(f"    {i:>2}. {col}")
            print()
            for field in mapping:
                label   = field.replace('_', ' ').title()
                current = mapping[field] or '(none)'
                val     = input(f"  '{label}' [{current}] — enter number/name or Enter to keep: ").strip()
                if val:
                    if val.isdigit() and 1 <= int(val) <= len(df.columns):
                        mapping[field] = df.columns[int(val) - 1]
                    elif val in df.columns:
                        mapping[field] = val
        return mapping

    # ── Select or create industry ─────────────────────────────────────────────

    def _select_industry(self, filename):
        fname = filename.lower()
        auto  = next((ind for ind in INDUSTRIES if ind.lower() in fname), None)

        print(f"\n  Select industry for '{filename}':")
        for i, ind in enumerate(INDUSTRIES, 1):
            tag = '  ← auto-detected' if ind == auto else ''
            print(f"    {i}. {ind}{tag}")
        print(f"    {len(INDUSTRIES)+1}. Add new industry")

        while True:
            default = str(INDUSTRIES.index(auto) + 1) if auto else ''
            prompt  = f"  Choose [{default}]: " if default else "  Choose: "
            val     = (input(prompt).strip() or default)
            if val.isdigit():
                idx = int(val) - 1
                if 0 <= idx < len(INDUSTRIES):
                    return INDUSTRIES[idx]
                elif idx == len(INDUSTRIES):
                    name = input("  Enter new industry name: ").strip().title()
                    if name:
                        INDUSTRIES.append(name)
                        return name
            print("  Invalid option.")

    # ── Core organize logic ───────────────────────────────────────────────────

    def _organize(self, df, mapping, industry):
        organized = pd.DataFrame()
        organized['source'] = industry

        for field, col in mapping.items():
            organized[field] = df[col].values if col else (0 if field == 'user_reviews' else None)

        organized['product_name'] = organized['product_name'].astype(str).str.strip()
        organized['brand']        = organized['brand'].astype(str).str.strip()
        organized['price']        = pd.to_numeric(organized['price'],        errors='coerce')
        organized['user_rating']  = pd.to_numeric(organized['user_rating'],  errors='coerce')
        organized['user_reviews'] = pd.to_numeric(organized['user_reviews'], errors='coerce').fillna(0).astype(int)

        before    = len(organized)
        organized = organized.dropna(subset=['price', 'user_rating']).reset_index(drop=True)
        dropped   = before - len(organized)
        if dropped:
            print(f"  ⚠  Dropped {dropped} rows with missing price/rating")

        organized['price_band']  = organized['price'].apply(_assign_price_band)
        organized['rating_tier'] = organized['user_rating'].apply(_assign_rating_tier)
        return organized

    # ── Merge into master dataset ─────────────────────────────────────────────

    def _merge(self, organized, industry):
        if os.path.exists(DATASET_PATH):
            existing       = pd.read_csv(DATASET_PATH)
            existing_count = len(existing[existing['source'] == industry])
            if existing_count > 0:
                print(f"\n  ⚠  Dataset already has {existing_count} rows for '{industry}'.")
                choice = input("  Replace existing? (y/n): ").strip().lower()
                if choice == 'y':
                    existing = existing[existing['source'] != industry]
            combined = pd.concat([existing, organized], ignore_index=True)
        else:
            combined = organized

        combined = combined.sort_values(
            ['source', 'brand', 'category', 'price_band', 'user_rating', 'user_reviews'],
            ascending=[True, True, True, True, False, False]
        ).reset_index(drop=True)

        combined['rank'] = range(1, len(combined) + 1)
        cols     = ['rank', 'source', 'product_name', 'brand', 'price',
                    'user_rating', 'user_reviews', 'category', 'price_band', 'rating_tier']
        combined = combined[[c for c in cols if c in combined.columns]]
        combined.to_csv(DATASET_PATH, index=False)
        return combined

    # ── Main entry point ──────────────────────────────────────────────────────

    def import_and_organize(self):
        print("\n── Import & Organize Data ──")

        # Step 1: Get file from user input or imports folder
        filepath, filename = self._get_csv_file()
        if not filepath:
            return

        try:
            df = pd.read_csv(filepath)
        except Exception as e:
            print(f"  ✗ Error reading file: {e}")
            return

        original_rows = len(df)
        print(f"\n  ✓ Loaded '{filename}': {original_rows} rows, {len(df.columns)} columns")

        # Step 2: Deduplicate — drop exact duplicate rows first
        before_dedup = len(df)
        df = df.drop_duplicates().reset_index(drop=True)
        if len(df) < before_dedup:
            print(f"  🔁 Removed {before_dedup - len(df)} duplicate rows (was {before_dedup})")

        # Step 3: Trim to 300
        if len(df) > MAX_ROWS:
            df = df.head(MAX_ROWS)
            print(f"  ✂  Trimmed to {MAX_ROWS} rows (was {len(df) + (before_dedup - len(df))})")
        else:
            print(f"  ✓ Under {MAX_ROWS} rows — no trimming needed")

        # Step 3: Select industry
        industry = self._select_industry(filename)

        # Step 4: Auto-map + confirm
        mapping = _auto_map(df.columns)
        mapping = self._confirm_mapping(df, mapping)

        # Step 5: Organize
        organized = self._organize(df, mapping, industry)

        # Step 6: Preview
        print(f"\n  Preview (first 3 rows):")
        print(f"  {'Product':<25} {'Brand':<20} {'Price':>8}  {'Rating':>6}  {'Category'}")
        print(f"  {'─'*75}")
        for _, row in organized.head(3).iterrows():
            print(f"  {str(row['product_name']):<25} {str(row['brand']):<20} "
                  f"${float(row['price']):>7.2f}  {float(row['user_rating']):>6.2f}  {str(row['category'])}")

        confirm = input(f"\n  Import {len(organized)} rows into '{industry}'? (y/n): ").strip().lower()
        if confirm != 'y':
            print("  Import cancelled.")
            return

        # Step 7: Merge & save-
        combined = self._merge(organized, industry)

        print(f"\n  ✓ Successfully imported {len(organized)} rows as '{industry}'!")
        print(f"  ✓ Dataset now has {len(combined)} total rows")
        print(f"\n  Brand breakdown for '{industry}':")
        for brand, count in organized['brand'].value_counts().head(10).items():
            print(f"    {str(brand):<25} {count} products")
