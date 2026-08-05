from analytics.database import get_connection


# ============================================================
# GET FILTER OPTIONS
# ============================================================

def get_filter_options():

    connection = get_connection()

    try:

        # Categories
        categories = connection.execute("""
            SELECT DISTINCT category
            FROM products
            WHERE category IS NOT NULL
            ORDER BY category
        """).fetchall()

        # Cities
        cities = connection.execute("""
            SELECT DISTINCT city
            FROM customers
            WHERE city IS NOT NULL
            ORDER BY city
        """).fetchall()

        # Products
        products = connection.execute("""
            SELECT DISTINCT product_name
            FROM products
            WHERE product_name IS NOT NULL
            ORDER BY product_name
        """).fetchall()

        # Date range
        dates = connection.execute("""
            SELECT
                MIN(order_date),
                MAX(order_date)
            FROM orders
        """).fetchone()

        return {
            "categories": [
                row[0] for row in categories
            ],

            "cities": [
                row[0] for row in cities
            ],

            "products": [
                row[0] for row in products
            ],

            "min_date": dates[0],

            "max_date": dates[1]
        }

    finally:

        connection.close()