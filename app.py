from flask import Flask, request
from flaskext.mysql import MySQL
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

mysql = MySQL()
mysql.init_app(app)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'test'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

# Create connection
conn = mysql.connect()




@app.route('/')
def hello_world():
    return 'Hello Wod!'


@app.route('/query', methods=['POST'])
def postQuery():
    # name = request.json["name"]
    # age = request.json["age"]
    query = request.json["query"]
    print(request.json)
    # Create cursor
    cursor = conn.cursor()
    # cursor.execute("insert into patient(name,age) values (%s,%s)", (name, age))
    cursor.execute(query)
    # cursor.execute(query)
    conn.commit()
    cursor.close()
    return 'hi'


if __name__ == '__main__':
    app.debug = True
    app.run()
    # app.run(debug=True)
