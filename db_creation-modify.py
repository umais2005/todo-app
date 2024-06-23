import sqlite3

conn = sqlite3.connect("todo.db")
cursor = conn.cursor()
cursor.execute(""" CREATE TABLE tasks(
                id INTEGER PRIMARY KEY ,
                priority VARCHAR,
                description VARCHAR UNIQUE,
                category VARCHAR,
                date DATE); """)
# cursor.execute("""
#     CREATE TABLE categories(
#     id INTEGER PRIMARY KEY,
#     category VARCHAR,
#     color VARCHAR UNIQUE);
# """)
conn.commit()
# list = cursor.fetchall()
# for record in list:
#     print(record)
