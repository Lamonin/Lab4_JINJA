import pandas as pd


def get_reader(conn):
    return pd.read_sql("SELECT * FROM reader", conn)


def get_book_reader(conn, reader_id):
    sql_query = f'''
        WITH reader_books AS (SELECT *
                              FROM book_reader
                                       JOIN book b on b.book_id = book_reader.book_id
                              WHERE reader_id = {reader_id}),
             book_authors AS (SELECT
                                  title AS "Книга",
                                  group_concat(author_name, ', ') AS "Авторы",
                                  borrow_date AS "Дата_выдачи",
                                  return_date AS "Дата_возврата"
                              FROM book_author
                                       JOIN reader_books USING (book_id)
                                       JOIN main.author USING (author_id)
                              GROUP BY book_reader_id, title
                              ORDER BY 1)
        SELECT *
        FROM book_authors;
    '''
    return pd.read_sql(sql_query, conn)
