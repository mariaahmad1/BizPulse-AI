from analytics.database import get_connection


def get_kpis():

    connection = get_connection()

    cursor = connection.cursor()

    # Total customers
    cursor.execute("""
        SELECT COUNT(*)
        FROM customers
    """)

    total_customers = cursor.fetchone()[0]


    # Total products
    cursor.execute("""
        SELECT COUNT(*)
        FROM products
    """)

    total_products = cursor.fetchone()[0]


    # Total orders
    cursor.execute("""
        SELECT COUNT(*)
        FROM orders
    """)

    total_orders = cursor.fetchone()[0]


    # Completed orders
    cursor.execute("""
        SELECT COUNT(*)
        FROM orders
        WHERE order_status = 'Completed'
    """)

    completed_orders = cursor.fetchone()[0]


    # Cancelled orders
    cursor.execute("""
        SELECT COUNT(*)
        FROM orders
        WHERE order_status = 'Cancelled'
    """)

    cancelled_orders = cursor.fetchone()[0]


    # Revenue
    cursor.execute("""
        SELECT
            SUM(
                oi.quantity *
                oi.unit_price
            )
        FROM order_items oi

        JOIN orders o
            ON oi.order_id = o.order_id

        WHERE o.order_status != 'Cancelled'
    """)

    total_revenue = cursor.fetchone()[0] or 0


    # Cost
    cursor.execute("""
        SELECT
            SUM(
                oi.quantity *
                p.cost_price
            )

        FROM order_items oi

        JOIN orders o
            ON oi.order_id = o.order_id

        JOIN products p
            ON oi.product_id = p.product_id

        WHERE o.order_status != 'Cancelled'
    """)

    total_cost = cursor.fetchone()[0] or 0


    # Profit
    total_profit = total_revenue - total_cost


    # Profit margin
    profit_margin = (
        (total_profit / total_revenue) * 100
        if total_revenue > 0
        else 0
    )


    # Units sold
    cursor.execute("""
        SELECT
            SUM(oi.quantity)

        FROM order_items oi

        JOIN orders o
            ON oi.order_id = o.order_id

        WHERE o.order_status != 'Cancelled'
    """)

    total_units_sold = cursor.fetchone()[0] or 0


    # Average order value
    average_order_value = (
        total_revenue / completed_orders
        if completed_orders > 0
        else 0
    )


    connection.close()


    return {
        "customers": total_customers,
        "products": total_products,
        "orders": total_orders,
        "completed_orders": completed_orders,
        "cancelled_orders": cancelled_orders,
        "revenue": total_revenue,
        "cost": total_cost,
        "profit": total_profit,
        "profit_margin": profit_margin,
        "units_sold": total_units_sold,
        "average_order_value": average_order_value
    }