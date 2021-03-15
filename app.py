from flask import Flask, request
from flaskext.mysql import MySQL
from flask_cors import CORS
from tokenization import Tokenization
from translation import Translation
from stemming import Stemming

app = Flask(__name__)
CORS(app)

#---------- MySQL configurations --------------
# mysql = MySQL()
# mysql.init_app(app)
#
# app.config['MYSQL_DATABASE_USER'] = 'root'
# app.config['MYSQL_DATABASE_PASSWORD'] = ''
# app.config['MYSQL_DATABASE_DB'] = 'test'
# app.config['MYSQL_DATABASE_HOST'] = 'localhost'
# mysql.init_app(app)
#
# # Create connection
# conn = mysql.connect()
#---------- MySQL configurations --------------

# Tokenization
tokenize = Tokenization()

# Translation
translator = Translation()

stemming = Stemming()

@app.route('/')
def hello_world():
    # a = tokenize.posTagger('සියලුම රෝගීන්ගේ විස්තර ලබා ගන්න')
    # b = translator.translate('සියලුම රෝගීන්ගේ විස්තර ලබා ගන්න', app)
    # stemming.findRoot('root')
    # file = open('sinhala_stemmer.txt', encoding='UTF-8')
    # lines = file.readlines()
    #
    # stemmer_dict = {}
    # for line in lines:
    #     line = line.split('\t')
    #     stemmer_dict[line[0].strip()] = line[1].strip('\n')
    # print(stemming.stemmer_dict)
    x = stemming.findRoot('සිසු')
    return x



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
