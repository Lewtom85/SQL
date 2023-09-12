#'ex_01_conection_to_db.py'
import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Connected to {db_file}, sqlite version: {sqlite3.version} ")
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def create_connection_in_memory():
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(":memory:")
        print(f"Connected, sqlite version: {sqlite3.version}")
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    create_connection(r"database.db")
    create_connection_in_memory()

create_projects_sql = """
--- prjcets table
CREATE TABLE IF NOT EXIST projects (
    id integer  PRIMARY KEY,
    nazwa text NOT NULL,    
    start_date text,
    end_date text
);
"""

create_task_sql = """
--- zadanie table
CREATE TABLE IF NOT EXIST tasks (
    id integer PRIMARY KEY,
    projekt_id integer NOT NULL,
    nazwa VARCHAR(250) NOT NULL,
    opis TEXT,
    status VARCHAR(15) NOT NULL,
    start_date text NOT NULL,
    end_date text NOT NULL,
    FOREIGN KEY (projekt_id) REFERENCES projects (id)
);
"""

from sqlite3 import Error

def execute_sql(conn, sql):
    """Execute sql
    :param conn: Connection object
    :param sql: a SQL script
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(sql)
    except Error as e:
        print(e)