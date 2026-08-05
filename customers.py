from analytics.database import get_connection


def get_top_customers(limit=10):

    connection = get_connection()

    query = """
        SELECT
            c.first_name,
            c.last_name,
            c.city,

            COUNT(
                DISTINCT o.order_id
            ) AS orders,

            SUM(
                oi.quantity *
                oi.unit_price
            ) AS total_spent

        FROM customers c

        JOIN orders o
            ON c.customer_id = o.customer_id

        JOIN order_items oi
            ON o.order_id = oi.order_id

        WHERE o.order_status != 'Cancelled'

        GROUP BY
            c.customer_id,
            c.first_name,
            c.last_name,
            c.city

        ORDER BY total_spent DESC

        LIMIT ?
    """

    result = connection.execute(
        query,
        (limit,)
    ).fetchall()

    connection.close()

    return result


def get_customer_summary():

    connection = get_connection()

    query = """
        SELECT
            customer_id,
            COUNT(order_id) AS order_count

        FROM orders

        WHERE order_status != 'Cancelled'

        GROUP BY customer_id
    """

    result = connection.execute(query).fetchall()

    connection.close()

    return result