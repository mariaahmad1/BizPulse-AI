from analytics.database import get_connection


def get_monthly_sales():

    connection = get_connection()

    query = """
        SELECT
            strftime('%Y-%m', o.order_date)
                AS month,

            SUM(
                oi.quantity *
                oi.unit_price
            ) AS revenue

        FROM orders o

        JOIN order_items oi
            ON o.order_id = oi.order_id

        WHERE o.order_status != 'Cancelled'

        GROUP BY month

        ORDER BY month
    """

    result = connection.execute(query).fetchall()

    connection.close()

    return result


def get_sales_by_category():

    connection = get_connection()

    query = """
        SELECT
            p.category,

            SUM(
                oi.quantity *
                oi.unit_price
            ) AS revenue

        FROM order_items oi

        JOIN orders o
            ON oi.order_id = o.order_id

        JOIN products p
            ON oi.product_id = p.product_id

        WHERE o.order_status != 'Cancelled'

        GROUP BY p.category

        ORDER BY revenue DESC
    """

    result = connection.execute(query).fetchall()

    connection.close()

    return result