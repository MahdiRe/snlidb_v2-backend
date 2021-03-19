from flaskext.mysql import MySQL

class Db:

    def __init__(self, app):
        self.configureDB(app)

    def configureDB(self, app):
        mysql = MySQL()
        mysql.init_app(app)

        app.config['MYSQL_DATABASE_USER'] = 'root'
        app.config['MYSQL_DATABASE_PASSWORD'] = ''
        app.config['MYSQL_DATABASE_DB'] = 'test'
        app.config['MYSQL_DATABASE_HOST'] = 'localhost'
        mysql.init_app(app)

        # Create connection
        self.conn = mysql.connect()

    def executeQuery(self, query):
        # Create cursor
        cursor = self.conn.cursor()
        # cursor.execute("insert into patient(name,age) values (%s,%s)", (name, age))
        cursor.execute(query)
        self.conn.commit()
        records = cursor.fetchall()
        cursor.close()
        return records
