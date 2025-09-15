
#
# Author: Rohtash Lakra
#
import sqlite3
from pathlib import Path

__UTF_8 = 'UTF-8'

# open database connection
connection = sqlite3.connect('posts.db')

cur_dir = Path(__file__).parent
print(f"cur_dir:{cur_dir}")
data_path = cur_dir.joinpath("data")
print(f"data_path:{data_path}")
print()

print("Opening database connection ...")
# read schema file and execute all the queries
with open(data_path.joinpath('schema.sql'), encoding=__UTF_8) as schema_file:
    connection.executescript(schema_file.read())

#cursor
# cursor = connection.cursor()

print("Initializing database ...")

# read init-db file to populate db
with open(data_path.joinpath('init-db.sql'), encoding=__UTF_8) as file:
    connection.executescript(file.read())
    # while line := file.readline():
    #     line = line.rstrip()
    #     print(line)
    #     cursor.execute(line)
    #     print()

print("Closing database connection ...")
# commit connection
connection.commit()
connection.close()

print("Database connection is closed.")
