import pandas as pd
import os

# ── Paths relative to this script's location ─────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))

nike       = pd.read_csv(os.path.join(BASE, "trimmed_nike_data_2022_09.csv"))
restaurant = pd.read_csv(os.path.join(BASE, "trimmed_restaurant_sales_malaysian_data.csv"))
starbucks  = pd.read_csv(os.path.join(BASE, "starbucks_drinks.csv"))
skincare   = pd.read_csv(os.path.join(BASE, "trimmed_skincare.csv"))
skincare   = skincare.drop_duplicates(subset=['product_id']).reset_index(drop=True)

nike['industry']       = 'Shoes'
restaurant['industry'] = 'Foods'
starbucks['industry']  = 'Coffee'
skincare['industry']   = 'Skincare'

# ── Keep only needed columns ─────────────────────────────────────────────────
# Shoes : brand = Nike (only 1 brand in dataset; new CSVs with Adidas/Puma etc. will add variety)
nike = nike[['industry', 'name', 'brand', 'price', 'avg_rating', 'review_count', 'sub_title']].copy()
nike.columns = ['industry', 'product_name', 'brand', 'price', 'user_rating', 'user_reviews', 'category']

# Foods : brand = restaurant_type (Casual Dining, Fine Dining, Street Food, Food Court, Fast Food)
restaurant = restaurant[['industry', 'menu_item_name', 'restaurant_type', 'actual_selling_price',
                          'quantity_sold', 'category', 'cuisine_type']].copy()
restaurant.columns = ['industry', 'product_name', 'brand', 'price', 'user_rating', 'user_reviews', 'category']

# Coffee : brand = Beverage_category (Classic Espresso, Signature Espresso, Frappuccino, Smoothies etc.)
starbucks = starbucks[['industry', 'Beverage', 'Beverage_category', 'Calories',
                        'Caffeine (mg)', 'Sugars (g)', 'Beverage_prep']].copy()
starbucks.columns = ['industry', 'product_name', 'brand', 'price', 'user_rating', 'user_reviews', 'category']

# Skincare : brand = brand_name (54 Thrones, Algenist, AERIN, Alpha-H, alpyn beauty etc.)
skincare = skincare[['industry', 'product_name', 'brand_name', 'price_usd',
                      'rating', 'reviews', 'primary_category']].copy()
skincare.columns = ['industry', 'product_name', 'brand', 'price', 'user_rating', 'user_reviews', 'category']

# ── Fix user_reviews per source BEFORE combining (avoids mixed-type errors) ──
nike['user_reviews']       = pd.to_numeric(nike['user_reviews'],       errors='coerce').fillna(0).astype(int)
restaurant['user_reviews'] = pd.to_numeric(restaurant['user_reviews'], errors='coerce').fillna(0).astype(int)
starbucks['user_reviews']  = pd.to_numeric(starbucks['user_reviews'],  errors='coerce').fillna(0).astype(int)
skincare['user_reviews']   = pd.to_numeric(skincare['user_reviews'],   errors='coerce').fillna(0).astype(int)

# ── Combine all into one DataFrame ───────────────────────────────────────────
df = pd.concat([nike, restaurant, starbucks, skincare], ignore_index=True)

# ── Clean data ───────────────────────────────────────────────────────────────
df['product_name'] = df['product_name'].str.strip()
df['brand']        = df['brand'].str.strip()
df['price']        = pd.to_numeric(df['price'], errors='coerce')
df['user_rating']  = pd.to_numeric(df['user_rating'], errors='coerce')

# ── Drop rows where price or rating is unusable for pd.cut ───────────────────
df = df.dropna(subset=['price', 'user_rating']).reset_index(drop=True)

# ── Add Price Band column ─────────────────────────────────────────────────────
df['price_band'] = pd.cut(
    df['price'],
    bins=[0, 25, 50, 100, 250, float('inf')],
    labels=['Budget ($0-25)', 'Mid ($26-50)', 'Premium ($51-100)', 'Luxury ($101-250)', 'Ultra ($250+)']
)

# ── Add Rating Tier column ────────────────────────────────────────────────────
df['rating_tier'] = pd.cut(
    df['user_rating'],
    bins=[0, 2.9, 3.9, 4.4, 5.0],
    labels=['Low (1-2.9)', 'Average (3-3.9)', 'Good (4-4.4)', 'Top Rated (4.5-5)']
)

# ── Sort by source → brand → category → price band → rating ──────────────────
df = df.sort_values(
    ['industry', 'brand', 'category', 'price_band', 'user_rating', 'user_reviews'],
    ascending=[True, True, True, True, False, False]
).reset_index(drop=True)

# ── Add rank column ───────────────────────────────────────────────────────────
df.insert(0, 'rank', range(1, len(df) + 1))

# ── Save next to this script ──────────────────────────────────────────────────
out_path = os.path.join(BASE, "all_industries_organized.csv")
df.to_csv(out_path, index=False)

print(f"\nSaved: {out_path}")
print(f"   Total rows  : {len(df)}")
print(f"   Columns     : {df.columns.tolist()}")
print(f"\n   Brand breakdown per industry:")
for industry, group in df.groupby('industry'):
    brands = group['brand'].unique()
    print(f"   {industry} ({len(brands)} brands): {', '.join(brands[:6])}{'...' if len(brands) > 6 else ''}")
