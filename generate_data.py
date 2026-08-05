
import sqlite3
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta


# ============================================================
# BIZPULSE AI - LUNA LANE DATA GENERATOR
# ============================================================

# -----------------------------
# CONFIGURATION
# -----------------------------

NUM_CUSTOMERS = 500
NUM_PRODUCTS = 50
NUM_ORDERS = 5000

DATABASE_PATH = "database/bizpulse.db"


# -----------------------------
# RANDOM DATA SETUP
# -----------------------------

random.seed(42)
np.random.seed(42)


# ============================================================
# 1. CUSTOMER DATA
# ============================================================

print("👥 Generating customers...")

first_names = [
    "Emma", "Olivia", "Ava", "Sophia", "Isabella",
    "Mia", "Amelia", "Harper", "Evelyn", "Luna",
    "Ella", "Grace", "Chloe", "Sofia", "Layla",
    "Nora", "Lily", "Hannah", "Aria", "Zoe"
]

last_names = [
    "Smith", "Johnson", "Williams", "Brown", "Jones",
    "Garcia", "Miller", "Davis", "Wilson", "Anderson",
    "Taylor", "Thomas", "Moore", "Martin", "Jackson",
    "White", "Harris", "Clark", "Lewis", "Young"
]

cities = [
    "New York", "Los Angeles", "Chicago", "Houston",
    "Miami", "London", "Toronto", "Sydney",
    "Dubai", "Singapore"
]

customers = []

start_date = datetime(2024, 1, 1)
end_date = datetime(2025, 12, 31)

for customer_id in range(1, NUM_CUSTOMERS + 1):

    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    city = random.choice(cities)

    email = (
        f"{first_name.lower()}."
        f"{last_name.lower()}"
        f"{customer_id}@example.com"
    )

    signup_date = start_date + timedelta(
        days=random.randint(
            0,
            (end_date - start_date).days
        )
    )

    customers.append({
        "customer_id": customer_id,
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "city": city,
        "signup_date": signup_date.date()
    })


customers_df = pd.DataFrame(customers)


# ============================================================
# 2. PRODUCT DATA
# ============================================================

print("👗 Generating products...")

product_catalog = {
    "Dresses": [
        "Classic Midi Dress",
        "Floral Summer Dress",
        "Satin Evening Dress",
        "Linen Maxi Dress",
        "Wrap Dress",
        "Pleated Dress",
        "Ribbed Knit Dress",
        "Velvet Party Dress"
    ],

    "Tops": [
        "Classic Cotton Tee",
        "Silk Blouse",
        "Oversized Shirt",
        "Ribbed Tank Top",
        "Linen Button-Up",
        "Cropped Top",
        "Satin Camisole"
    ],

    "Bottoms": [
        "Wide Leg Trousers",
        "Classic Straight Jeans",
        "High Waist Pants",
        "Linen Shorts",
        "Pleated Skirt",
        "Denim Skirt",
        "Tailored Pants"
    ],

    "Bags": [
        "Classic Black Tote",
        "Mini Shoulder Bag",
        "Leather Crossbody",
        "Quilted Handbag",
        "Canvas Tote",
        "Evening Clutch"
    ],

    "Shoes": [
        "Classic White Sneakers",
        "Leather Loafers",
        "Block Heel Sandals",
        "Pointed Toe Heels",
        "Ankle Boots",
        "Ballet Flats"
    ],

    "Accessories": [
        "Gold Hoop Earrings",
        "Minimalist Necklace",
        "Classic Watch",
        "Silk Hair Scarf",
        "Leather Belt",
        "Sunglasses"
    ]
}


price_ranges = {
    "Dresses": (45, 180),
    "Tops": (20, 90),
    "Bottoms": (35, 120),
    "Bags": (40, 200),
    "Shoes": (50, 180),
    "Accessories": (10, 80)
}


products = []

for product_id in range(1, NUM_PRODUCTS + 1):

    category = random.choice(
        list(product_catalog.keys())
    )

    product_name = random.choice(
        product_catalog[category]
    )

    min_price, max_price = price_ranges[category]

    price = round(
        random.uniform(
            min_price,
            max_price
        ),
        2
    )

    cost_price = round(
        price * random.uniform(
            0.40,
            0.70
        ),
        2
    )

    stock_quantity = random.randint(
        5,
        150
    )

    reorder_level = random.randint(
        10,
        30
    )

    products.append({
        "product_id": product_id,
        "product_name": product_name,
        "category": category,
        "price": price,
        "cost_price": cost_price,
        "stock_quantity": stock_quantity,
        "reorder_level": reorder_level
    })


products_df = pd.DataFrame(products)


# ============================================================
# 3. ORDER DATA
# ============================================================

print("🛒 Generating orders...")

orders = []
order_items = []

order_statuses = [
    "Completed",
    "Completed",
    "Completed",
    "Completed",
    "Shipped",
    "Processing",
    "Cancelled"
]


for order_id in range(1, NUM_ORDERS + 1):

    customer_id = random.randint(
        1,
        NUM_CUSTOMERS
    )

    order_date = start_date + timedelta(
        days=random.randint(
            0,
            (end_date - start_date).days
        )
    )

    order_status = random.choice(
        order_statuses
    )

    orders.append({
        "order_id": order_id,
        "customer_id": customer_id,
        "order_date": order_date.date(),
        "order_status": order_status
    })

    # Generate 1-4 products per order

    number_of_items = random.randint(
        1,
        4
    )

    selected_products = random.sample(
        range(1, NUM_PRODUCTS + 1),
        number_of_items
    )

    for product_id in selected_products:

        product_price = products_df.loc[
            products_df["product_id"] == product_id,
            "price"
        ].iloc[0]

        quantity = random.randint(
            1,
            3
        )

        order_items.append({
            "order_item_id": len(order_items) + 1,
            "order_id": order_id,
            "product_id": product_id,
            "quantity": quantity,
            "unit_price": product_price
        })


orders_df = pd.DataFrame(orders)

order_items_df = pd.DataFrame(
    order_items
)


# ============================================================
# 4. INVENTORY DATA
# ============================================================

print("📦 Generating inventory...")

inventory = []

for _, product in products_df.iterrows():

    last_restock_date = start_date + timedelta(
        days=random.randint(
            0,
            (end_date - start_date).days
        )
    )

    inventory.append({
        "inventory_id": int(
            product["product_id"]
        ),
        "product_id": int(
            product["product_id"]
        ),
        "quantity_in_stock": int(
            product["stock_quantity"]
        ),
        "last_restock_date":
            last_restock_date.date()
    })


inventory_df = pd.DataFrame(
    inventory
)


# ============================================================
# 5. CONNECT TO DATABASE
# ============================================================

print("🗄️ Connecting to database...")

connection = sqlite3.connect(
    DATABASE_PATH
)


# ============================================================
# 6. INSERT DATA INTO DATABASE
# ============================================================

print("💾 Saving data to database...")

customers_df.to_sql(
    "customers",
    connection,
    if_exists="append",
    index=False
)

products_df.to_sql(
    "products",
    connection,
    if_exists="append",
    index=False
)

orders_df.to_sql(
    "orders",
    connection,
    if_exists="append",
    index=False
)

order_items_df.to_sql(
    "order_items",
    connection,
    if_exists="append",
    index=False
)

inventory_df.to_sql(
    "inventory",
    connection,
    if_exists="append",
    index=False
)


# ============================================================
# 7. CLOSE DATABASE
# ============================================================

connection.close()


# ============================================================
# 8. FINAL SUMMARY
# ============================================================

print("\n" + "=" * 50)

print("🎉 BIZPULSE AI DATA GENERATION COMPLETE!")

print("=" * 50)

print(
    f"👥 Customers created: "
    f"{len(customers_df)}"
)

print(
    f"👗 Products created: "
    f"{len(products_df)}"
)

print(
    f"🛒 Orders created: "
    f"{len(orders_df)}"
)

print(
    f"🧾 Order items created: "
    f"{len(order_items_df)}"
)

print(
    f"📦 Inventory records created: "
    f"{len(inventory_df)}"
)

print("\n🚀 Luna Lane is ready for analysis!")