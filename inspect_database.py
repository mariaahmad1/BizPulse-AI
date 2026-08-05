import sqlite3
import os

DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "database",
    "bizpulse.db"
)

connection = sqlite3.connect(DB_PATH)

tables = connection.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type='table'
    ORDER BY name
""").fetchall()

print("\n================ DATABASE TABLES ================\n")

for table in tables:

    table_name = table[0]

    print(f"\n📋 TABLE: {table_name}")
    print("-" * 50)

    columns = connection.execute(
        f"PRAGMA table_info({table_name})"
    ).fetchall()

    for column in columns:

        print(
            f"Column: {column[1]} | "
            f"Type: {column[2]} | "
            f"Primary Key: {column[5]}"
        )

    print()

connection.close()

print("\n✅ DATABASE INSPECTION COMPLETE!")