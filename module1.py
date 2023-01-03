import socket
import HTTP_Server
import sqlite3
import SQLtoJson

# conn = sqlite3.connect("WebRoot/db/movie1.db")
# c = conn.cursor()
# c.execute("""CREATE TABLE movie1(
#             comments text
#             )""")
# conn.commit()
# conn.close()

class DB:
    def __init__(self, data):
        print(data + "&&&&&")
        conn = sqlite3.connect("WebRoot/db/movie1.db")
        c = conn.cursor()
        c.execute("INSERT INTO movie1 VALUES ('{}')".format(data))
        conn.commit()
        conn.close()
        SQLtoJson.SQLtoJson()
        print("aaaa")