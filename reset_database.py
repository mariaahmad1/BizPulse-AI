import sqlite3

DATABASE_PATH = "database/bizpulse.db"

# Connect to the database
connection = sqlite3.connect(DATABASE_PATH)

cursor = connection.cursor()

# Delete all existing data
cursor.execute("DELETE FROM order_items")
cursor.execute("DELETE FROM orders")
cursor.execute("DELETE FROM inventory")
cursor.execute("DELETE FROM products")
cursor.execute("DELETE FROM customers")

# Save changes
connection.commit()

# Close connection
connection.close()

print("🧹 Database reset successfully!")
print("✅ All old business data has been removed.")
print("🚀 Ready to generate fresh Luna Lane data!")