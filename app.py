from flask import Flask, request
from flask_cors import CORS
from tokenization import Tokenization
from translation import Translation
from stemming import Stemming
from db import Db

app = Flask(__name__)
CORS(app)
db = Db(app)

tokenizer = Tokenization()
translator = Translation(app)

# test = 'සියලුම සිසුන්ගේ තොරතුරු ලබා දෙන්න'
# test1 = 'ලකුනු 75ට සමාන වැඩි සිසුන්ගේ නම් නම සුනිල් දත්ත තොරතුරු හෝඅඩු'
t1 = "සියලුම සිසුන්ගේ තොරතුරු ලබාදෙන්න"
t2 = "සියලුම සිසුන්ගේ නම ලබාදෙන්න"
t3 = "සුනිල්ගේ විස්තර ලබාදෙන්න"
t4 = "ලකුනු 75ට වැඩි සිසුන්ගේ විස්තර ලබාදෙන්න"
t5 = "ලකුනු 75ක් ගත් සිසුන්ගේ විස්තර ලබාදෙන්න"
t6 = "වයස 14 වු  සිසුන්ගේ විස්තර ලබාදෙන්න"
t7 = "ලකුනු 75ක් හෝඅඩු සිසුන්ගේ විස්තර ලබාදෙන්න"

@app.route('/')
def hello_world():

    # Tokenization + Stemming + POS Tagging
    tags = tokenizer.posTagger(t4)
    print('tokens: ' + str(tags))

    # Derive the Command, Table, Columns, Logics and Conditions
    command, table, columns, logics, conditions = '', '', [], [], []
    for tag in tags[0]:
        query = "SELECT english_word,semantic_meaning FROM word_mappings WHERE sinhala_word='"+tag[0]+"' OR root_word='"+tag[0]+"';"
        result = db.executeQuery(query)
        for i in result:
            if i[1] != 'neglect':
                if i[1] == 'command':
                    command = i[0]
                elif i[1] == 'table':
                    table = i[0]
                elif i[1] == 'column':
                    columns.append((tag[0], i[1]))
                elif i[1] == 'logic':
                    logics.append((tag[0], i[1]))
                elif i[1] == 'condition':
                    conditions.append((tag[0], i[1]))

    # Replace the logics
    print('columns' + str(columns))
    print('logics' + str(logics))
    print('conditions' + str(conditions))

    t4_con = t4
    for con in conditions:
        t4_con.replace(con[0], con[1])

    ab = command + ' ' + str(columns) + ' FROM ' + table
    return t4_con


# @app.route('/query', methods=['POST'])
# def generateQuery():
#     query = request.json['query']
#     # tags = tokenize.posTagger(query)
#     # print(tags[0])
#     # for tag in tags[0]:
#         print(tag)
#         # print(tag[0] + ', ' + stemming.findRoot(tag[0]))
#
#     # x = db.executeQuery("insert into patient(name,age) values ('gg',17)")
#     return 'test'

@app.route('/a')
def a():
    stem = Stemming()
    print(stem.findRoot('මකන්න'))
    print(stem.findRoot('ඉවත්'))
    print(stem.findRoot('යාවත්කාලීන'))
    print(stem.findRoot('ඇතුළු'))
    print(stem.findRoot('වෙනස්'))
    print(stem.findRoot('මාරු'))
    print(stem.findRoot('ඇතුලත්'))
    # print(tokenize.posTagger(t1))
    # print(tokenize.posTagger(t2))
    # print(tokenize.posTagger(t3))
    # print(tokenize.posTagger(t4))
    # print(tokenize.posTagger(t5))
    # print(tokenize.posTagger(t6))
    # print(tokenize.posTagger(t7))
    return 'hello'




if __name__ == '__main__':
    app.run(debug=True)
