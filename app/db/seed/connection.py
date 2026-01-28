from .pw import get_connection

def get_db_connection():
    con = get_connection()
    con.autocommit = True
    return con