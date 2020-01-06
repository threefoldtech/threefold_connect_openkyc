import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file, check_same_thread=False)
        return conn
    except Error as e:
        print(e)

    return None

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        alter_table(conn, "ALTER TABLE users ADD COLUMN signed_email_identifier text NULL;")
    except Error as e:
        print(e)
  
def alter_table(conn, alter_table_sql):
    try:
        c = conn.cursor()
        res = c.execute(alter_table_sql)
        print("Added column to sqlite.")
    except Error as e:
        print(e)
        print("Table already exists. All good.")

def insert_user(conn, user_id, email, verification_code, verified, public_key, signed_email_identifier):
    try:
        insert_user_sql = "INSERT INTO users (user_id, email, verification_code, verified, public_key, signed_email_identifier) VALUES (?,?,?,?,?,?);"
        c = conn.cursor()
        c.execute(insert_user_sql,(user_id, email, verification_code, verified, public_key, signed_email_identifier))
        conn.commit()
    except Error as e:
        print(e)

def update_user_verification_code(conn, user_id, verification_code):
    try:
        update_sql = "UPDATE users SET verification_code = ? WHERE user_id = ?;"
        c = conn.cursor()
        c.execute(update_sql,(verification_code, user_id))
        conn.commit()
    except Error as e:
        print(e)

def delete_user(conn, user_id, email):
    try:
        delete_user_sql = "DELETE FROM users WHERE user_id = ? AND email = ?;"
        c = conn.cursor()
        c.execute(delete_user_sql, (user_id, email))
        conn.commit()
    except Error as e:
        print(e)

def select_all(conn,select_all_users):
    try:
        c = conn.cursor()
        c.execute(select_all_users)
        rows = c.fetchall()

        for row in rows:
            print(row)
    except Error as e:
        print(e)

def update_user(conn,update_sql,*params):
    try:
        c = conn.cursor()
        if len(params)==2:
            c.execute(update_sql,(params[0],params[1]))
            conn.commit()
        elif len(params)==3:
            c.execute(update_sql,(params[0],params[1],params[2]))
            conn.commit()
    except Error as e:
        print(e)

def getUserByName(conn, user_id):
    print('Getting user by id', user_id)
    find_statement="SELECT * FROM users WHERE user_id=? LIMIT 1;"
    try:
        c = conn.cursor()
        c.execute(find_statement,(user_id,))
        return c.fetchone()
    except Error as e:
        print(e)

def create_db(conn):
    sql_create_user_table = """CREATE TABLE IF NOT EXISTS users (user_id text NOT NULL UNIQUE,email text NOT NULL,verification_code text NOT NULL, verified integer,public_key text NOT NULL,signed_email_identifier text NULL); """
    if conn is not None:
        create_table(conn, sql_create_user_table)
    else:
        print("Error! cannot create the database connection.")

