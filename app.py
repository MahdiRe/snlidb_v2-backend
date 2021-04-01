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


# @app.route('/query', methods=['POST'])
# def generateQuery():
#     query = request.json['query']
#     print(query)
#     # result = queryGenerator.generateSQL(query)
#     return result


@app.route('/query/v2', methods=['POST'])
def generateQueryV2():
    query = request.json['query']
    print(query)
    nlq = SQLBuilder(query)
    nlq.pos_tagging()
    nlq.semantic_analysis()
    nlq.derive_conditions()
    nlq.derive_updates()
    nlq.refine_columns()
    nlq.reserve_sql_words()
    nlq.arrange_sql_words()
    print(nlq.sql_)
    # result = queryGenerator.generateSQL(query)
    return nlq.sql_


@app.route('/execute', methods=['POST'])
def executeQuery():
    query = request.json['query']
    print(query)
    result = studentRepo.executeQuery(query)
    return json.dumps(result)


@app.route('/tokenize')
def tokenize():
    x = str(tokenizer.posTagger(a1)) + "\n" + str(tokenizer.posTagger(a2)) + "\n" + str(
        tokenizer.posTagger(a3)) + "\n" + str(tokenizer.posTagger(a4))
    print(x)
    # return str(tokenizer.posTagger("වැඩියෙන්"))
    return x


if __name__ == '__main__':
    app.run(debug=True)
