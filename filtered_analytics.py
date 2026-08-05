import sqlite3
import os


# ============================================================
# DATABASE CONNECTION
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


def get_connection():
    return sqlite3.connect(DB_PATH)


# ============================================================
# BUILD FILTER CONDITIONS
# ============================================================

def build_filters(
    start_date=None,
    end_date=None,
    category="All Categories",
    city="All Cities",
    product="All Products"
):

    conditions = [
        "o.order_status != 'Cancelled'"
    ]

    params = []

    if start_date:
        conditions.append(
            "o.order_date >= ?"
        )
        params.append(
            str(start_date)
        )

    if end_date:
        conditions.append(
            "o.order_date <= ?"
        )
        params.append(
            str(end_date)
        )

    if category and category != "All Categories":
        conditions.append(
            "p.category = ?"
        )
        params.append(
            category
        )

    if city and city != "All Cities":
        conditions.append(
            "c.city = ?"
        )
        params.append(
            city
        )

    if product and product != "All Products":
        conditions.append(
            "p.product_name = ?"
        )
        params.append(
            product
        )

    return (
        " AND ".join(conditions),
        params
    )


# ============================================================
# FILTERED KPIs
# ============================================================

def get_filtered_kpis(
    start_date=None,
    end_date=None,
    category="All Categories",
    city="All Cities",
    product="All Products"
):

    connection = get_connection()

    try:

        where_clause, params = build_filters(
            start_date,
            end_date,
            category,
            city,
            product
        )

        query = f"""
        SELECT

            COUNT(
                DISTINCT o.order_id
            ) AS orders,

            COUNT(
                DISTINCT o.customer_id
            ) AS customers,

            COALESCE(
                SUM(
                    oi.quantity *
                    oi.unit_price
                ),
                0
            ) AS revenue,

            COALESCE(
                SUM(
                    oi.quantity *
                    p.cost_price
                ),
                0
            ) AS cost,

            COALESCE(
                SUM(
                    oi.quantity
                ),
                0
            ) AS units_sold

        FROM orders o

        JOIN order_items oi
            ON o.order_id = oi.order_id

        JOIN products p
            ON oi.product_id = p.product_id

        JOIN customers c
            ON o.customer_id = c.customer_id

        WHERE {where_clause}
        """

        result = connection.execute(
            query,
            params
        ).fetchone()

        orders = result[0] or 0
        customers = result[1] or 0
        revenue = result[2] or 0
        cost = result[3] or 0
        units_sold = result[4] or 0

        profit = revenue - cost

        profit_margin = (
            (profit / revenue) * 100
            if revenue > 0
            else 0
        )

        average_order_value = (
            revenue / orders
            if orders > 0
            else 0
        )

        return {
            "orders": orders,
            "customers": customers,
            "revenue": revenue,
            "cost": cost,
            "profit": profit,
            "profit_margin": profit_margin,
            "units_sold": units_sold,
            "average_order_value": average_order_value
        }

    finally:

        connection.close()


# ============================================================
# FILTERED MONTHLY SALES
# ============================================================

def get_filtered_monthly_sales(
    start_date=None,
    end_date=None,
    category="All Categories",
    city="All Cities",
    product="All Products"
):

    connection = get_connection()

    try:

        where_clause, params = build_filters(
            start_date,
            end_date,
            category,
            city,
            product
        )

        query = f"""
        SELECT

            strftime(
                '%Y-%m',
                o.order_date
            ) AS month,

            SUM(
                oi.quantity *
                oi.unit_price
            ) AS revenue

        FROM orders o

        JOIN order_items oi
            ON o.order_id = oi.order_id

        JOIN products p
            ON oi.product_id = p.product_id

        JOIN customers c
            ON o.customer_id = c.customer_id

        WHERE {where_clause}

        GROUP BY month

        ORDER BY month
        """

        return connection.execute(
            query,
            params
        ).fetchall()

    finally:

        connection.close()


# ============================================================
# FILTERED CATEGORY SALES
# ============================================================

def get_filtered_category_sales(
    start_date=None,
    end_date=None,
    category="All Categories",
    city="All Cities",
    product="All Products"
):

    connection = get_connection()

    try:

        where_clause, params = build_filters(
            start_date,
            end_date,
            category,
            city,
            product
        )

        query = f"""
        SELECT

            p.category,

            SUM(
                oi.quantity *
                oi.unit_price
            ) AS revenue

        FROM orders o

        JOIN order_items oi
            ON o.order_id = oi.order_id

        JOIN products p
            ON oi.product_id = p.product_id

        JOIN customers c
            ON o.customer_id = c.customer_id

        WHERE {where_clause}

        GROUP BY p.category

        ORDER BY revenue DESC
        """

        return connection.execute(
            query,
            params
        ).fetchall()

    finally:

        connection.close()


# ============================================================
# FILTERED TOP PRODUCTS
# ============================================================

def get_filtered_top_products(
    limit=10,
    start_date=None,
    end_date=None,
    category="All Categories",
    city="All Cities",
    product="All Products"
):

    connection = get_connection()

    try:

        where_clause, params = build_filters(
            start_date,
            end_date,
            category,
            city,
            product
        )

        query = f"""
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

        FROM orders o

        JOIN order_items oi
            ON o.order_id = oi.order_id

        JOIN products p
            ON oi.product_id = p.product_id

        JOIN customers c
            ON o.customer_id = c.customer_id

        WHERE {where_clause}

        GROUP BY
            p.product_id,
            p.product_name,
            p.category

        ORDER BY revenue DESC

        LIMIT ?
        """

        params.append(limit)

        return connection.execute(
            query,
            params
        ).fetchall()

    finally:

        connection.close()


# ============================================================
# FILTERED TOP CUSTOMERS
# ============================================================

def get_filtered_top_customers(
    limit=10,
    start_date=None,
    end_date=None,
    category="All Categories",
    city="All Cities",
    product="All Products"
):

    connection = get_connection()

    try:

        where_clause, params = build_filters(
            start_date,
            end_date,
            category,
            city,
            product
        )

        query = f"""
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

        FROM orders o

        JOIN customers c
            ON o.customer_id = c.customer_id

        JOIN order_items oi
            ON o.order_id = oi.order_id

        JOIN products p
            ON oi.product_id = p.product_id

        WHERE {where_clause}

        GROUP BY
            c.customer_id,
            c.first_name,
            c.last_name,
            c.city

        ORDER BY total_spent DESC

        LIMIT ?
        """

        params.append(limit)

        return connection.execute(
            query,
            params
        ).fetchall()

    finally:

        connection.close()