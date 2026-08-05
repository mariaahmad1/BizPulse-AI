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
# GET AI BUSINESS INSIGHTS
# ============================================================

def generate_ai_insights():

    connection = get_connection()

    insights = []

    try:

        # ====================================================
        # 1. OVERALL PROFITABILITY
        # ====================================================

        profitability_query = """
        SELECT
            SUM(oi.quantity * oi.unit_price) AS revenue,
            SUM(
                oi.quantity * p.cost_price
            ) AS total_cost
        FROM order_items oi
        INNER JOIN products p
            ON oi.product_id = p.product_id
        INNER JOIN orders o
            ON oi.order_id = o.order_id
        WHERE o.order_status = 'Completed'
        """

        profitability = connection.execute(
            profitability_query
        ).fetchone()

        revenue = profitability[0] or 0
        total_cost = profitability[1] or 0
        profit = revenue - total_cost

        if revenue > 0:

            profit_margin = (
                profit / revenue
            ) * 100

        else:

            profit_margin = 0


        # ====================================================
        # PROFITABILITY INSIGHT
        # ====================================================

        if profit_margin >= 40:

            insights.append({
                "type": "success",
                "title": "💰 Strong Profitability",
                "message": (
                    f"Your business generated "
                    f"${profit:,.2f} in estimated profit "
                    f"with a {profit_margin:.1f}% profit margin. "
                    f"This indicates strong overall profitability."
                )
            })

        elif profit_margin >= 20:

            insights.append({
                "type": "info",
                "title": "📊 Healthy Profitability",
                "message": (
                    f"Your business currently has a "
                    f"{profit_margin:.1f}% profit margin. "
                    f"Consider optimizing costs and pricing "
                    f"to improve profitability further."
                )
            })

        else:

            insights.append({
                "type": "warning",
                "title": "⚠️ Profitability Needs Attention",
                "message": (
                    f"Your current profit margin is "
                    f"{profit_margin:.1f}%. "
                    f"Review product costs, pricing, "
                    f"and operational expenses."
                )
            })


        # ====================================================
        # 2. MOST PROFITABLE CATEGORY
        # ====================================================

        category_query = """
        SELECT
            p.category,
            SUM(
                oi.quantity *
                (oi.unit_price - p.cost_price)
            ) AS profit

        FROM order_items oi

        INNER JOIN products p
            ON oi.product_id = p.product_id

        INNER JOIN orders o
            ON oi.order_id = o.order_id

        WHERE o.order_status = 'Completed'

        GROUP BY p.category

        ORDER BY profit DESC

        LIMIT 1
        """

        top_category = connection.execute(
            category_query
        ).fetchone()


        if top_category:

            category = top_category[0]
            category_profit = top_category[1]

            insights.append({
                "type": "success",
                "title": "🏆 Top Profit Category",
                "message": (
                    f"{category} is currently your "
                    f"most profitable category, generating "
                    f"approximately ${category_profit:,.2f} "
                    f"in profit. Consider prioritizing this "
                    f"category for inventory and marketing."
                )
            })


        # ====================================================
        # 3. MOST PROFITABLE PRODUCT
        # ====================================================

        product_query = """
        SELECT
            p.product_name,
            p.category,
            SUM(
                oi.quantity *
                (oi.unit_price - p.cost_price)
            ) AS profit

        FROM order_items oi

        INNER JOIN products p
            ON oi.product_id = p.product_id

        INNER JOIN orders o
            ON oi.order_id = o.order_id

        WHERE o.order_status = 'Completed'

        GROUP BY
            p.product_id,
            p.product_name,
            p.category

        ORDER BY profit DESC

        LIMIT 1
        """

        top_product = connection.execute(
            product_query
        ).fetchone()


        if top_product:

            product_name = top_product[0]
            product_category = top_product[1]
            product_profit = top_product[2]

            insights.append({
                "type": "success",
                "title": "⭐ Highest-Profit Product",
                "message": (
                    f"{product_name} in the "
                    f"{product_category} category is your "
                    f"most profitable product, generating "
                    f"approximately ${product_profit:,.2f} "
                    f"in profit. Consider maintaining healthy "
                    f"stock levels for this product."
                )
            })


        # ====================================================
        # 4. INVENTORY ALERT
        # ====================================================

        inventory_query = """
        SELECT
            COUNT(*)

        FROM inventory i

        INNER JOIN products p
            ON i.product_id = p.product_id

        WHERE i.quantity_in_stock <= p.reorder_level
        """

        low_stock_count = connection.execute(
            inventory_query
        ).fetchone()[0]


        if low_stock_count > 0:

            insights.append({
                "type": "warning",
                "title": "📦 Inventory Risk Detected",
                "message": (
                    f"{low_stock_count} products are "
                    f"currently at or below their reorder "
                    f"level. Review these products and "
                    f"prioritize restocking high-demand items."
                )
            })

        else:

            insights.append({
                "type": "success",
                "title": "📦 Healthy Inventory",
                "message": (
                    "No products are currently below "
                    "their reorder levels. Inventory "
                    "levels appear healthy."
                )
            })


        # ====================================================
        # 5. CUSTOMER INSIGHT
        # ====================================================

        customer_query = """
        SELECT
            COUNT(DISTINCT customer_id)

        FROM orders

        WHERE order_status = 'Completed'
        """

        active_customers = connection.execute(
            customer_query
        ).fetchone()[0]


        insights.append({
            "type": "info",
            "title": "👥 Customer Activity",
            "message": (
                f"Your business has "
                f"{active_customers:,} customers "
                f"with completed orders. "
                f"Consider loyalty campaigns and "
                f"personalized offers to encourage "
                f"repeat purchases."
            )
        })


        # ====================================================
        # 6. STRATEGIC RECOMMENDATION
        # ====================================================

        insights.append({
            "type": "info",
            "title": "🚀 Strategic Recommendation",
            "message": (
                "Focus your next business decisions on "
                "three areas: protect your highest-margin "
                "products, maintain inventory for high-demand "
                "items, and increase customer retention "
                "through targeted loyalty strategies."
            )
        })


        return insights


    finally:

        connection.close()