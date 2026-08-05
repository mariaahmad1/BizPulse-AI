import sqlite3

DATABASE_PATH = "database/bizpulse.db"


def get_connection():
    """
    Create and return a connection
    to the BizPulse AI database.
    """
    return sqlite3.connect(DATABASE_PATH)