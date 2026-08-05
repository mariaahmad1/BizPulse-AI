
import sqlite3

# ============================================================
# BIZPULSE AI - PRODUCT PERFORMANCE ANALYSIS
# ============================================================

DATABASE_PATH = "database/bizpulse.db"

# Connect to database
connection = sqlite3.connect(DATABASE_PATH)

cursor = connection.cursor()

print("🎉 Connected to BizPulse AI database!")


# ============================================================
# 1. TOP 10 BEST-SELLING PRODUCTS
# ============================================================

print("\n" + "=" * 60)
print("🏆 TOP 10 BEST-SELLING PRODUCTS")
print("=" * 60)

cursor.execute("""
SELECT
    p.product_name,
    p.category,
    SUM(oi.quantity) AS units_sold,
    SUM(oi.quantity * oi.unit_price) AS revenue
FROM order_items oi
JOIN orders o
    ON oi.order_id = o.order_id
JOIN products p
    ON oi.product_id = p.product_id
WHERE o.order_status != 'Cancelled'
GROUP BY
    p.product_id,
    p.product_name,
    p.category
ORDER BY units_sold DESC
LIMIT 10
""")

best_sellers = cursor.fetchall()

for rank, product in enumerate(
    best_sellers,
    start=1
):

    product_name = product[0]
    category = product[1]
    units_sold = product[2]
    revenue = product[3]

    print(
        f"{rank}. {product_name} "
        f"({category}) | "
        f"Units: {units_sold:,} | "
        f"Revenue: ${revenue:,.2f}"
    )


# ============================================================
# 2. TOP 10 PRODUCTS BY REVENUE
# ============================================================

print("\n" + "=" * 60)
print("💰 TOP 10 PRODUCTS BY REVENUE")
print("=" * 60)

cursor.execute("""
SELECT
    p.product_name,
    p.category,
    SUM(oi.quantity * oi.unit_price) AS revenue,
    SUM(oi.quantity) AS units_sold
FROM order_items oi
JOIN orders o
    ON oi.order_id = o.order_id
JOIN products p
    ON oi.product_id = p.product_id
WHERE o.order_status != 'Cancelled'
GROUP BY
    p.product_id,
    p.product_name,
    p.category
ORDER BY revenue DESC
LIMIT 10
""")

top_revenue_products = cursor.fetchall()

for rank, product in enumerate(
    top_revenue_products,
    start=1
):

    product_name = product[0]
    category = product[1]
    revenue = product[2]
    units_sold = product[3]

    print(
        f"{rank}. {product_name} "
        f"({category}) | "
        f"Revenue: ${revenue:,.2f} | "
        f"Units: {units_sold:,}"
    )


# ============================================================
# 3. SLOWEST-SELLING PRODUCTS
# ============================================================

print("\n" + "=" * 60)
print("🐌 10 SLOWEST-SELLING PRODUCTS")
print("=" * 60)

cursor.execute("""
SELECT
    p.product_name,
    p.category,
    COALESCE(SUM(oi.quantity), 0) AS units_sold,
    COALESCE(
        SUM(oi.quantity * oi.unit_price),
        0
    ) AS revenue
FROM products p
LEFT JOIN order_items oi
    ON p.product_id = oi.product_id
LEFT JOIN orders o
    ON oi.order_id = o.order_id
    AND o.order_status != 'Cancelled'
GROUP BY
    p.product_id,
    p.product_name,
    p.category
ORDER BY units_sold ASC
LIMIT 10
""")

slow_products = cursor.fetchall()

for rank, product in enumerate(
    slow_products,
    start=1
):

    product_name = product[0]
    category = product[1]
    units_sold = product[2]
    revenue = product[3]

    print(
        f"{rank}. {product_name} "
        f"({category}) | "
        f"Units: {units_sold:,} | "
        f"Revenue: ${revenue:,.2f}"
    )


# ============================================================
# 4. PRODUCT PROFIT MARGIN
# ============================================================

print("\n" + "=" * 60)
print("📊 TOP PRODUCTS BY PROFIT MARGIN")
print("=" * 60)

cursor.execute("""
SELECT
    p.product_name,
    p.category,

    SUM(
        oi.quantity *
        (oi.unit_price - p.cost_price)
    ) AS profit,

    SUM(
        oi.quantity * oi.unit_price
    ) AS revenue,

    (
        SUM(
            oi.quantity *
            (oi.unit_price - p.cost_price)
        )
        /
        SUM(
            oi.quantity * oi.unit_price
        )
    ) * 100 AS profit_margin

FROM order_items oi

JOIN orders o
    ON oi.order_id = o.order_id

JOIN products p
    ON oi.product_id = p.product_id

WHERE o.order_status != 'Cancelled'

GROUP BY
    p.product_id,
    p.product_name,
    p.category

HAVING revenue > 0

ORDER BY profit_margin DESC

LIMIT 10
""")

margin_products = cursor.fetchall()

for rank, product in enumerate(
    margin_products,
    start=1
):

    product_name = product[0]
    category = product[1]
    profit = product[2]
    revenue = product[3]
    margin = product[4]

    print(
        f"{rank}. {product_name} "
        f"({category}) | "
        f"Margin: {margin:.2f}% | "
        f"Profit: ${profit:,.2f}"
    )


# ============================================================
# 5. CLOSE DATABASE
# ============================================================

connection.close()


print("\n" + "=" * 60)
print("🚀 PRODUCT PERFORMANCE ANALYSIS COMPLETE!")
print("=" * 60)