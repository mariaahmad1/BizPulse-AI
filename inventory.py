import sqlite3
import os


# ============================================================
# DATABASE PATH
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DB_PATH = os.path.join(
    BASE_DIR,
    "database",
    "bizpulse.db"
)


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():

    return sqlite3.connect(DB_PATH)


# ============================================================
# GET COMPLETE INVENTORY STATUS
# ============================================================

def get_inventory_status():

    connection = get_connection()

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

        result = connection.execute(
            query
        ).fetchall()

        return result

    finally:

        connection.close()


# ============================================================
# GET LOW STOCK PRODUCTS
# ============================================================

def get_low_stock_products():

    connection = get_connection()

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

    WHERE i.quantity_in_stock <= p.reorder_level

    ORDER BY i.quantity_in_stock ASC
    """

    try:

        result = connection.execute(
            query
        ).fetchall()

        return result

    finally:

        connection.close()


# ============================================================
# INVENTORY SUMMARY
# ============================================================

def get_inventory_summary():

    connection = get_connection()

    query = """
    SELECT

        COUNT(*) AS total_products,

        COALESCE(
            SUM(i.quantity_in_stock),
            0
        ) AS total_stock,

        SUM(
            CASE
                WHEN i.quantity_in_stock <= p.reorder_level
                THEN 1
                ELSE 0
            END
        ) AS low_stock_products

    FROM inventory i

    INNER JOIN products p
        ON i.product_id = p.product_id
    """

    try:

        result = connection.execute(
            query
        ).fetchone()

        return {

            "total_products":
                result[0] or 0,

            "total_stock":
                result[1] or 0,

            "low_stock_products":
                result[2] or 0

        }

    finally:

        connection.close()