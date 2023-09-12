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

def create_tables(conn):
    """Create the projects and tasks tables if they don't exist."""
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
    CREATE TABLE IF NOT EXISTS tasks (
        id integer PRIMARY KEY,
        project_id integer NOT NULL,
        nazwa VARCHAR(250) NOT NULL,
        opis TEXT,
        status VARCHAR(15) NOT NULL,
        start_date text NOT NULL,
        end_date text NOT NULL,
        FOREIGN KEY (project_id) REFERENCES projects (id)
    );
    """
    
    execute_sql(conn, create_projects_sql)
    execute_sql(conn, create_task_sql)

def add_project(conn, project):
    """Create a new project and add it to the projects table.
    :param conn: Connection object
    :param project: Tuple containing project data
    :return: Project ID
    """
    sql = '''INSERT INTO projects(nazwa, start_date, end_date)
            VALUES(?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, project)
    conn.commit()
    return cur.lastrowid

def add_task(conn, task):
    """Create a new task and add it to the tasks table.
    :param conn: Connection object
    :param task: Tuple containing task data
    :return: Task ID
    """
    sql = '''INSERT INTO tasks(project_id, nazwa, opis, status, start_date, end_date)
            VALUES(?,?,?,?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()
    return cur.lastrowid

def select_task_by_status(conn, status):
    """Query tasks by status.
    :param conn: Connection object
    :param status: Status to filter tasks
    :return: List of task records
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks WHERE status=?", (status,))
    rows = cur.fetchall()
    return rows

def select_all(conn, table):
    """Query all rows in a table.
    :param conn: Connection object
    :param table: Table name to query
    :return: List of records
    """
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table}")
    rows = cur.fetchall()
    return rows

def select_where(conn, table, **query):
    """Query rows from a table with specified conditions.
    :param conn: Connection object
    :param table: Table name to query
    :param query: Dictionary of attributes and values to filter by
    :return: List of records
    """
    cur = conn.cursor()
    qs = []
    values = ()
    for k, v in query.items():
        qs.append(f"{k}=?")
        values += (v,)
    q = " AND ".join(qs)
    cur.execute(f"SELECT * FROM {table} WHERE {q}", values)
    rows = cur.fetchall()
    return rows

def update(conn, table, id, **kwargs):
    """Update rows in a table.
    :param conn: Connection object
    :param table: Table name to update
    :param id: ID of the row to update
    :param kwargs: Dictionary of columns and values to update
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
        cur.execute(sql, values)
        conn.commit()
        print("OK")
    except sqlite3.OperationalError as e:
        print(e)

def delete_where(conn, table, **kwargs):
    """Delete rows from a table based on specified conditions.
    :param conn: Connection object
    :param table: Table name to delete from
    :param kwargs: Dictionary of attributes and values to filter by for deletion
    """
    qs = []
    values = tuple()
    for k, v in kwargs.items():
        qs.append(f"{k}=?")
        values += (v,)
    q = " AND ".join(qs)

    sql = f'DELETE FROM {table} WHERE {q}'
    cur = conn.cursor()
    cur.execute(sql, values)
    conn.commit()
    print("Deleted")

def delete_all(conn, table):
    """Delete all rows from a table.
    :param conn: Connection object
    :param table: Table name to delete from
    """
    sql = f'DELETE FROM {table}'
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    print("Deleted")

if __name__ == "__main__":
    db_file = "database.db"
    
    conn = create_connection(db_file)
    if conn is not None:
        create_tables(conn)

        project = ("Powtorka z angielskiego", "2020-05-11 00:00:00", "2020-05-13 00:00:00")
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

        print(f"Project ID: {pr_id}, Task ID: {task_id}")

        tasks = select_task_by_status(conn, "started")
        print("Tasks with status 'started':", tasks)

        all_tasks = select_all(conn, "tasks")
        print("All tasks:", all_tasks)

        specific_tasks = select_where(conn, "tasks", status="started", project_id=1)
        print("Specific tasks:", specific_tasks)

        update(conn, "tasks", 2, status="in progress")

        tasks_before_deletion = select_all(conn, "tasks")
        print("Tasks before deletion:", tasks_before_deletion)

        delete_where(conn, "tasks", id=3)
        tasks_after_deletion = select_all(conn, "tasks")
        print("Tasks after deletion with id=3:", tasks_after_deletion)

        delete_all(conn, "tasks")
        tasks_after_all_deletion = select_all(conn, "tasks")
        print("Tasks after all deletion:", tasks_after_all_deletion)

        conn.close()
    else:
        print("Error! Cannot create the database connection.")

