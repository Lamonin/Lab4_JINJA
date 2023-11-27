import pandas as pd


def get_guests(conn):
    sql_query = '''
        SELECT DISTINCT guest_name FROM guest ORDER BY 1;
    '''
    return pd.read_sql(sql_query, conn)


def get_statuses(conn):
    sql_query = '''
        SELECT (
                   CASE
                       WHEN status_name = 'Занят' THEN 'Проживал(а)'
                       WHEN status_name = 'Забронирован' THEN 'Бронировал(а)'
                       WHEN status_name = 'Бронирование отменено' THEN 'Отменил(а) бронирование'
                       END
                   ) AS 'Статус'
        FROM status
        UNION ALL
        SELECT 'Не проживал(а)' AS 'Статус';
    '''
    return pd.read_sql(sql_query, conn)


def get_guest_booking_status(conn, guest_name=None, status_name=None):
    sql_query = f'''
        WITH guest_booking_status AS (
            SELECT guest_name AS 'Фамилия',
               (
                   CASE
                       WHEN status_name = 'Занят' THEN 'Проживал(а)'
                       WHEN status_name = 'Забронирован' THEN 'Бронировал(а)'
                       WHEN status_name = 'Бронирование отменено' THEN 'Отменил(а) бронирование'
                       ELSE 'Не проживал(а)'
                       END
                   )      AS 'Статус',
               (
                   CASE
                       WHEN COUNT(status_name) = 0 THEN '-'
                       ELSE COUNT(*)
                       END
                   )      AS 'Количество'
        FROM guest
                 LEFT JOIN room_booking USING (guest_id)
                 LEFT JOIN status USING (status_id)
        {f"WHERE guest_name == '{guest_name}'" if guest_name else ''}
        GROUP BY 1, 2
        )
        SELECT *
        FROM guest_booking_status
        {f"WHERE Статус == '{status_name}'" if status_name else ''}
        ORDER BY 1, 2 DESC;
    '''

    return pd.read_sql(sql_query, conn)