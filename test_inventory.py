import sqlite3
import os

DB_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "database",
    "bizpulse.db"
)

print("DATABASE BEING USED:")
print(DB_PATH)

print("\n========================================")
print("TESTING INVENTORY QUERY")
print("========================================")

connection = sqlite3.connect(DB_PATH)

query = """
SELECT
    p.product_id,
    p.product_name,
    p.category,
    i.quantity_in_stock,
    p.reorder_level,
    p.price,
    p.cost_price,
    i.last_restock_date

FROM inventory i

INNER JOIN products p
    ON i.product_id = p.product_id

ORDER BY i.quantity_in_stock ASC
"""

try:

    results = connection.execute(query).fetchall()

    print("\n✅ INVENTORY QUERY WORKED!")
    print(f"Total records: {len(results)}")

    print("\nFirst 5 records:")

    for row in results[:5]:
        print(row)

except Exception as error:

    print("\n❌ INVENTORY QUERY FAILED!")
    print(error)

finally:

    connection.close()