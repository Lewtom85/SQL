# ex_02_create_tables.py

import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """Create a database connection to the SQLite database specified by db_file.
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    
    return conn

def execute_sql(conn, sql):
    """Execute SQL
    :param conn: Connection object
    :param sql: SQL script
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(sql)
    except Error as e:
        print(e)

if __name__ == "__main__":
    create_projects_sql = """
    -- projects table
    CREATE TABLE IF NOT EXISTS projects (
        id integer PRIMARY KEY,
        nazwa text NOT NULL,
        start_date text,
        end_date text
    );
    """

    create_task_sql = """
    -- task table
    CREATE TABLE IF NOT EXISTS task (
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

    db_file = "database.db"

    conn = create_connection(db_file)
    if conn is not None:
        execute_sql(conn, create_projects_sql)
        execute_sql(conn, create_task_sql)
        conn.close()

def add_project(conn, project):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    sql = '''INSERT INTO prjects(nazwa, start_date, end_date)
            VALUES(?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, prject)
    return cur.lastrowid

conn = create_connection("database.db")
project = ("Powtorka z angielskiego", "2020-05-11 00:00:00", "2020-05-13 00:00:00")
pr_id = add_project(conn, project)
conn.commit()
return cur.lastrowid