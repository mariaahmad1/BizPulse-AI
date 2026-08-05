from analytics.database import get_connection


def get_top_products(limit=10):

    connection = get_connection()

    query = """
        SELECT
            p.product_name,

            p.category,

            SUM(
                oi.quantity
            ) AS units_sold,

            SUM(
                oi.quantity *
                oi.unit_price
            ) AS revenue,

            SUM(
                oi.quantity *
                (
                    oi.unit_price -
                    p.cost_price
                )
            ) AS profit

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

        LIMIT ?
    """

    result = connection.execute(
        query,
        (limit,)
    ).fetchall()

    connection.close()

    return result


def get_category_performance():

    connection = get_connection()

    query = """
        SELECT
            p.category,

            SUM(
                oi.quantity
            ) AS units_sold,

            SUM(
                oi.quantity *
                oi.unit_price
            ) AS revenue,

            SUM(
                oi.quantity *
                (
                    oi.unit_price -
                    p.cost_price
                )
            ) AS profit

        FROM order_items oi

        JOIN orders o
            ON oi.order_id = o.order_id

        JOIN products p
            ON oi.product_id = p.product_id

        WHERE o.order_status != 'Cancelled'

        GROUP BY p.category

        ORDER BY profit DESC
    """

    result = connection.execute(query).fetchall()

    connection.close()

    return result