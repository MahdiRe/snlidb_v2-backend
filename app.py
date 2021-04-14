from flask import Flask, request
from flask_cors import CORS
from service.tokenization import Tokenization
# from service.query_generator import QueryGenerator
from repository.student_repo import StudentRepo
import json
from model.sql_builder import SQLBuilder

app = Flask(__name__)
CORS(app)
tokenizer = Tokenization()
# queryGenerator = QueryGenerator()
studentRepo = StudentRepo()

# test = 'සියලුම සිසුන්ගේ තොරතුරු ලබා දෙන්න'
# test1 = 'ලකුනු 75ට සමාන වැඩි සිසුන්ගේ නම් නම සුනිල් දත්ත තොරතුරු හෝඅඩු'
# t1 = "සියලුම සිසුන්ගේ තොරතුරු ලබාදෙන්න"
# t2 = "සියලුම සිසුන්ගේ නම ලබාදෙන්න"
# t3 = "සුනිල්ගේ විස්තර ලබාදෙන්න"
# t31 = "නම සුනිල්ට සමාන  විස්තර ලබාදෙන්න"
# t32 = "නම සුනිල් වන සිසුන්ගේ විස්තර ලබාදෙන්න"
# t51 = "ලකුනු 75ට වැඩි සිසුන්ගේ විස්තර ලබාදෙන්න ලකුනු 75ක් ගත් වයස 14 වු ලකුනු 75ක් හෝඅඩු ලබාදෙන්න"
# t4 = "ලකුනු 75ට වැඩි සිසුන්ගේ විස්තර ලබාදෙන්න"
# t5 = "ලකුනු 75ක් ගත් සිසුන්ගේ විස්තර ලබාදෙන්න"
# t6 = "වයස 14 වු  සිසුන්ගේ විස්තර ලබාදෙන්න"
# t7 = "ලකුනු 75ක් හෝඅඩු සිසුන්ගේ විස්තර ලබාදෙන්න"
# t77 = "ලකුනු 75 හෝඅඩු සිසුන්ගේ විස්තර ලබාදෙන්න"
# t8 = "ලකුනු 75 හෝ ඊට වැඩි සිසුන්ගේ විස්තර ලබාදෙන්න"
# t9 = "ලකුනු 75ක් හෝවැඩි සිසුන්ගේ විස්තර ලබාදෙන්න"
# t10 = "ලකුනු 75 හෝවැඩි සිසුන්ගේ විස්තර ලබාදෙන්න"

a1 = "නම සුනිල් වයස 45 ලකුනු 50 ලෙස"
a2 = "නම සුනිල්"
a3 = "වයස 45"
a4 = "ලකුනු 50"


@app.route('/')
def hello_world():
    return 'Hello World!'


# ++++++++++++ Tables API's (3) ++++++++++++
@app.route('/tables')
def get_tables():
    tables = studentRepo.get_all_tables()
    i = 0
    while i < len(tables):
        if tables[i]['table_name'] == 'word_mappings':
            del tables[i]
        i = i + 1
    return json.dumps(tables)


@app.route('/tables/<table>')
def get_table_data(table):
    data = studentRepo.get_table_data(str(table))
    json_data = json.dumps(data, ensure_ascii=False).encode('UTF-8').decode()
    return json_data


@app.route('/tables/<table>/columns')
def get_columns(table):
    columns = studentRepo.get_columns(table)
    i = 0
    while i < len(columns):
        if columns[i]['COLUMN_NAME'] == 'id':
            del columns[i]
        i = i + 1
    json_data = json.dumps(columns, ensure_ascii=False).encode('UTF-8').decode()
    print(json_data)
    return json_data


@app.route('/tables/<table>/insert', methods=['POST'])
def insert_into_table(table):
    print(request.json)
    name = request.json['name']
    age = request.json['age']
    marks = request.json['marks']
    result = studentRepo.insert_student(name, age, marks)
    print(str(result))
    return str(result)


# ++++++++++++ Generate Query API's ++++++++++++
@app.route('/query/generate', methods=['POST'])
def generate_query():
    query = request.json['query']
    print(query)
    nlq = SQLBuilder(query)
    return nlq.nlq2sql_converter()
    # nlq.nlq2sql_converter()
    # return nlq.get_sql()


@app.route('/query/execute', methods=['POST'])
def execute_query():
    sql = request.json['sql']
    print(sql)
    result = studentRepo.execute_query(sql)
    json_data = json.dumps(result, ensure_ascii=False).encode('UTF-8').decode()
    return json_data


# @app.route('/query', methods=['POST'])
# def generateQuery():
#     query = request.json['query']
#     print(query)
#     # result = queryGenerator.generateSQL(query)
#     return result

# @app.route('/tokenize')
# def tokenize():
#     x = str(tokenizer.pos_tagger(a1)) + "\n" + str(tokenizer.pos_tagger(a2)) + "\n" + str(
#         tokenizer.pos_tagger(a3)) + "\n" + str(tokenizer.pos_tagger(a4))
#     print(x)
#     # return str(tokenizer.posTagger("වැඩියෙන්"))
#     return x


if __name__ == '__main__':
    app.run(debug=True)
