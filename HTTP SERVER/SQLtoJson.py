import sqlite3
import json

class SQLtoJson:
    def __init__(self):
        # modify path to sqlite db
        self.pathToSqliteDb = 'WebRoot/db/movie1.db'
        self.sqliteToJson()

    def dict_factory(self,cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    # connect to the SQlite databases
    def openConnection(self,pathToSqliteDb):
        connection = sqlite3.connect(pathToSqliteDb)
        connection.row_factory = self.dict_factory
        cursor = connection.cursor()
        return connection, cursor


    def getAllRecordsInTable(self,table_name, pathToSqliteDb):
        conn, curs = self.openConnection(pathToSqliteDb)
        conn.row_factory = self.dict_factory
        curs.execute("SELECT * FROM '{}' ".format(table_name))
        # fetchall as result
        results = curs.fetchall()
        # close connection
        conn.close()
        return json.dumps(results)


    def sqliteToJson(self):
        connection, cursor = self.openConnection(self.pathToSqliteDb)
        # select all the tables from the database
        # cursor.execute("SELECT * FROM movie1")
        # tables = cursor.fetchall()
            # Get the records in table
        results = self.getAllRecordsInTable('movie1', self.pathToSqliteDb)

            # generate and save JSON files with the table name for each of the database tables and save in results folder
        with open('WebRoot/results/movie1.json', 'w') as the_file:
            the_file.write(results)
        # close connection
        connection.close()

if __name__ == "__main__":
    SQLtoJson()
