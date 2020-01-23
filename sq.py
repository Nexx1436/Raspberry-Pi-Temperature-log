import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
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


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)



def select_task(conn, sql,params):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """
    cur = conn.cursor()
    cur.execute(sql, params)

    rows = cur.fetchall()
    return rows

def create_task(conn, task):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """

    sql = ''' INSERT INTO tasks(temp,hum,date)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, task)
    return cur.lastrowid


database = "kiss.db"

sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS tasks (
                                id integer PRIMARY KEY,
                                temp integer NOT NULL,
                                hum integer NOT NULL,
                                date text NOT NULL
                            );"""

# create a database connection
conn = create_connection(database)

# create tables
if conn is not None:
    # create tasks table
    create_table(conn, sql_create_tasks_table)
else:
    print("Error! cannot create the database connection.")

print(create_task(conn, (15, 20, "2020-01-22 19:43:36")))
select_task(conn,"SELECT * FROM tasks WHERE date like ?",(date))
conn.commit()
