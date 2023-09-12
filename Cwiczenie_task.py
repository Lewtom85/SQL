#ex_03.py
import sqlite3

def create_connection(db_file):
    """ create a database connection do the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

def add_project(conn, project):
    """
    Create a new project into the project table
    :param conn:
    :param project:
    :return: project id
    """
    sql = '''INSERT INTO projects(nazwa, start_date, end_date)
                VALUES(?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, project)
    conn.commit()
    return cur.lastrowid

def add_task(conn, task):
    """
    Create a new task into the task table
    :param conn:
    :param task:
    :return: task id
    """
    sql = '''INSERT INTO task(project_id, nazwa, opis, status, start_date, end_date)
                VALUES(?,?,?,?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()
    return cur.lastrowid

if __name__ == "__main__":
    project = ("Powtorka z angielskiego", "2020-05-11 00:00:00", "2020-05-13 00:00:00")

    conn = create_connection("database.db")
    pr_id = add_project(conn, project)

    task = (
        pr_id,
        "Czasowniki regularne",
        "Zapamietaj czasowniki ze strony 30",
        "started",
        "2020-05-11 12:00:00",
        "2020-05-11 15:00:00"
    )

    task_id = add_task(conn, task)

    print(pr_id, task_id)
    conn.commit()

#Kolejne zadanie, pobieranie danych
conn = create_connection("database.db")
cur = conn.cursor()
cur.execute("SELECT * FROM task")
rows = cur.fetchall()

rows

#Funkcja wykorzystujca kod

def select_task_by_status(conn, status):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param status:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks WHERE status=?", (status,))

    rows = cur.fetchall()
    return rows

#Funkcje select all and select where

def select_all(conn, table):
    """
    Query all rows in the table
    :param conn: the Conection object
    :return:
    """
    cur = conn.cursor()
    cur.execute(F"SELECT * FROM {table}")
    rows = cur. fetchall()

    return rows

def select_where(conn, table, **query):
    """
    Query tasks from table with data from **query dict
    :param conn: the Connection object
    :param table: table name
    :param query: dict of arributes and values
    :return:
    """
    cur = conn.cursor()
    qs = []
    values = ()
    for k, v in query.items():
        qs.append(f"{k}=?")
        values += (v,)
    q = " AND ".join(qs)
    cur.execute(f"SELECT * FROM {table} WHERE {q}, values")
    rows = cur.fetchall()
    return rows

#UPDATE

import sqlite 3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection do the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try: 
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    
    return conn

def update(conn, table, id, **kwargs):
    """
    update status, begin_date, and end date of a task
    :param conn:
    :param table: table name
    :param id: row id
    :return:
    """

    parameters = [f"{k} =?" for k in kwargs]
    parameters = ", ".join(parameters)
    values = tuple(v for v in kwargs.values())
    values += (id, )

    sql = f''' UPDATE {table}
                SET {parameters}
                WHERE id = ?'''
    try:
        cur = conn.cursor()
        cur.ecesute(sql, values)
        conn.commit()
        print("OK")
    except sqlite3.OperationlError as e:
        print(e)

if __name__ == "__main__":
    conn = create_connection("database.db")
    update(conn, "tasks", 2, status="started")
    update(conn, "tasks", 2, stat="started")
    conn.close()
    
