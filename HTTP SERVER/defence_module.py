import sqlite3
import re
import SQLtoJson
import module1

class DEFENCE:
    def __init__(self):
        conn = sqlite3.connect("WebRoot/db/movie1.db")
        c = conn.cursor()
        data = c.execute("""SELECT * FROM 'movie1'""")
        list = data.fetchall()
        for item in list:
            print(item)
            if re.search("[!@#$%^&*<>]+.*[!@#$%^&*<>]+", item[0]):
                print(item[0])
                print("a")
                c.execute(f"""DELETE FROM movie1 WHERE comments = '{item[0]}'""")
                conn.commit()
            else:
                print("b")
        SQLtoJson.SQLtoJson()
        conn.close()
    def check_insert(self,data):
        if re.search("[!@#$%^&*<>]+.*[!@#$%^&*<>]+", data):
            return False
        return True
