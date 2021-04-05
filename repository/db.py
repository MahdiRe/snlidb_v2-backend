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
