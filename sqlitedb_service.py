import sqlite3
from sqlite3 import Error
import datetime
import config_service

def get_connection():

    db_file = config_service.get_value('sqlite','database')

    print("DB FILE", db_file)

    conn = sqlite3.connect(db_file)

    return conn


def init_service():

    sql_create_transpo_record = """ CREATE TABLE IF NOT EXISTS transport_record (
                                    id integer PRIMARY KEY,
                                    action_type text,
                                    terminal_key text NOT NULL,
                                    card_id text NOT NULL,
                                    driver_id text,
                                    driver_name text,
                                    latitude float,
                                    longitude float,
                                    location_id text,
                                    timestamp text,
                                    latest_balance decimal(10,2) default 0.0,
                                    synched boolean default false
                                ); """;

    conn = get_connection()

    if conn is not None:
        create_table(sql_create_transpo_record)
        return conn
    else:
        print("Error! cannot create the database connection.")
    return None


def create_table(create_table_sql):

    conn = get_connection()

    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def insert_record(terminal_key, action_type, card_id, latitude, longitude, location_id, latest_balance, driver_id, driver_name):

    conn = get_connection()

    insertSQLTemplate = """INSERT INTO transport_record (terminal_key,action_type,card_id,latitude,longitude,location_id,timestamp,latest_balance,driver_id,driver_name)
                VALUES('{terminal_key_param}','{action_type_param}','{card_id_param}',{latitude_param},{longitude_param},'{location_id_param}',
                datetime('now', 'localtime'),{latest_balance_param},'{driver_id_param}','{driver_name_param}' ); """;

    insertSQL = insertSQLTemplate.format(
        terminal_key_param = terminal_key,
        action_type_param = action_type,
        card_id_param = card_id,
        latitude_param = latitude,
        longitude_param = longitude,
        location_id_param = location_id,
        latest_balance_param = latest_balance,
        driver_id_param = driver_id,
        driver_name_param = driver_name
        )

    print(insertSQL)

    try:
        c = conn.cursor()
        c.execute(insertSQL)
        conn.commit()
    except Error as e:
        print(e)


def get_recent_transactions(limit = 10):

    conn = get_connection()

    query = """SELECT * FROM transport_record order by timestamp desc limit {limit_param} ; """.format(limit_param = limit);

    print(query)

    try:
        c = conn.cursor()
        c.execute(query)
    except Error as e:
        print(e)

    rows = c.fetchall()

    #for row in rows:
    #    print(row)
    return rows

def test():

    # create a database connection
    init_service()

    conn = get_connection()

    if conn is not None:

           # test insert 
        insert_record('TRM1','BAL_INQUIRY','AB-CD-EF-01',14.628417,121.044691, 'DROPOFF001',1000.0, 'DRV001','Juan Dela Cruz')

        rows = get_recent_transactions()

        for row in rows:
            print(row)

    else:
        print("Error! cannot create the database connection.")

    conn.close()


if __name__ == '__main__':
    test()
