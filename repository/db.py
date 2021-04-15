from flask import Flask
from flaskext.mysql import MySQL


class Db:

    def __init__(self):
        self._conn = None
        self.configure_db(Flask(__name__))

    def configure_db(self, app):
        mysql = MySQL()
        mysql.init_app(app)

        app.config['MYSQL_DATABASE_USER'] = 'root'
        app.config['MYSQL_DATABASE_PASSWORD'] = ''
        app.config['MYSQL_DATABASE_DB'] = 'test'
        app.config['MYSQL_DATABASE_HOST'] = 'localhost'
        mysql.init_app(app)

        # Create connection
        self._conn = mysql.connect()

    def get_all_tables(self):
        try:
            cursor = self._conn.cursor()
            cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_type = %s AND "
                           "table_schema=%s;", ('base table', 'test'))
            self._conn.commit()
            tables = [dict((cursor.description[i][0], value)
                           for i, value in enumerate(row)) for row in cursor.fetchall()]
            cursor.close()

        except Exception as e:
            print('Exception : ' + str(e))
            tables = 'Exception found!'
        return tables

    def get_table_data(self, table):
        try:
            # Create cursor
            cursor = self._conn.cursor()
            cursor.execute("SELECT * FROM " + table + ";")
            self._conn.commit()
            data = [dict((cursor.description[i][0], value)
                         for i, value in enumerate(row)) for row in cursor.fetchall()]
            cursor.close()

        except Exception as e:
            print('Exception : ' + str(e))
            if e.args[0] == 1146:
                data = "Table '" + table + "' not found!"
            else:
                data = 'Exception found!'
        return data

    def get_columns(self, table):
        try:
            cursor = self._conn.cursor()
            cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = %s", table)
            self._conn.commit()
            columns = [dict((cursor.description[i][0], value)
                            for i, value in enumerate(row)) for row in cursor.fetchall()]
            cursor.close()
        except Exception as e:
            print('Exception : ' + str(e))
            columns = 'Exception found!'
        return columns

    def execute_query(self, query):
        try:
            cursor = self._conn.cursor()
            cursor.execute(query)
            self._conn.commit()
            result = cursor.fetchall()
            cursor.close()
        except Exception as e:
            print('Exception : ' + str(e))
            result = 'Exception found!'
        return result
