import sqlite3
from sqlite3 import Error
import datetime


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def init_service():
    
    database = r"db/hub.db"
    
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

    
    conn = create_connection(database)
    
    if conn is not None:
        create_table(conn, sql_create_transpo_record)
        return conn
    else:
        print("Error! cannot create the database connection.")
  
    return None

def create_table(conn, create_table_sql):

    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def insert_record(conn, terminal_key, action_type, card_id, latitude, longitude, location_id, latest_balance, driver_id, driver_name):
    
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

def get_recent_transactions(conn, limit = 10):
    
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
    conn = init_service()
    

    if conn is not None:

           # test insert 
        insert_record(conn,'TRM1','BAL_INQUIRY','AB-CD-EF-01',14.628417,121.044691, 'DROPOFF001',1000.0, 'DRV001','Juan Dela Cruz')
        
        rows = get_recent_transactions(conn)
        
        for row in rows:
            print(row)
        

    else:
        print("Error! cannot create the database connection.")
        
    conn.close()
        

if __name__ == '__main__':
    test()
