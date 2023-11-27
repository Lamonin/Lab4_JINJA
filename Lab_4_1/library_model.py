import pandas as pd


table_names = ["publisher", "genre", "book", "book_author", "author", "book_reader", "reader"]


def get_table(conn, table_name):
    return pd.read_sql(f"SELECT * FROM {table_name}", conn)


def get_all_tables(conn):
    # return {"publisher":get_table(conn, "publisher")}
    return {name: pd.read_sql(f"SELECT * FROM {name}", conn) for name in table_names}
