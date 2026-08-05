
import sqlite3

# Connect to our BizPulse AI database
connection = sqlite3.connect("database/bizpulse.db")

# Create a cursor to execute SQL commands
cursor = connection.cursor()

# ==========================================
# 1. CUSTOMERS TABLE
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    city TEXT,
    signup_date DATE NOT NULL
)
""")

# ==========================================
# 2. PRODUCTS TABLE
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL,
    cost_price REAL NOT NULL,
    stock_quantity INTEGER NOT NULL,
    reorder_level INTEGER NOT NULL
)
""")

# ==========================================
# 3. ORDERS TABLE
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    order_date DATE NOT NULL,
    order_status TEXT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
)
""")

# ==========================================
# 4. ORDER ITEMS TABLE
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS order_items (
    order_item_id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
)
""")

# ==========================================
# 5. INVENTORY TABLE
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS inventory (
    inventory_id INTEGER PRIMARY KEY,
    product_id INTEGER NOT NULL,
    quantity_in_stock INTEGER NOT NULL,
    last_restock_date DATE,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
)
""")

# Save all changes
connection.commit()

# Confirm everything was created
print("🎉 BizPulse AI database created successfully!")
print("✅ Customers table created")
print("✅ Products table created")
print("✅ Orders table created")
print("✅ Order Items table created")
print("✅ Inventory table created")

# Close the connection
connection.close()