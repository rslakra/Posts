#
# Author: Rohtash Lakra
#
import sqlite3

# connecting to database
connection = sqlite3.connect('database.db')

# Open Schema
with open('./liquibase/changesets/sql/create-tables.sql') as file:
    connection.executescript(file.read())

cur = connection.cursor()

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('First Post', 'Content for the first post')
            )

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('Second Post', 'Content for the second post')
            )

connection.commit()
connection.close()