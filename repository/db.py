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
            # Create cursor
            cursor = self._conn.cursor()
            cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_type = %s AND "
                           "table_schema=%s;", ('base table', 'test'))
            # cursor.execute("SELECT * from student")
            self._conn.commit()
            # tables = cursor.fetchall()
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
            # cursor.execute("SELECT * from student")
            self._conn.commit()
            # tables = cursor.fetchall()
            data = [dict((cursor.description[i][0], value)
                         for i, value in enumerate(row)) for row in cursor.fetchall()]
            cursor.close()

        except Exception as e:
            print('Exception : ' + str(e))
            data = 'Exception found!'
        return data
