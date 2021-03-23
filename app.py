from flask import Flask, request
from flask_cors import CORS
from tokenization import Tokenization
# from translation import Translation
# from stemming import Stemming
# from condition_extractor import ConditionExtractor
# from db import Db
# import nltk
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
from nltk import pos_tag, word_tokenize, RegexpParser
from service import Service

app = Flask(__name__)
CORS(app)
# db = Db(app)
# condition_ex = ConditionExtractor()
tokenizer = Tokenization()
# translator = Translation(app)
service = Service(app)

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


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/query', methods=['POST'])
def generateQuery():
    query = request.json['query']
    print(query)
    result = service.generateSQL(query)
    return result


@app.route('/tokenize')
def tokenize():
    return str(tokenizer.posTagger("වැඩියෙන්"))


@app.route('/parsetree')
def parsetree():
#     # Example text
#     sample_text = "The quick brown fox jumps over the lazy dog"
#
#     # Find all parts of speech in above sentence
#     tagged = pos_tag(word_tokenize(sample_text))
#
#     print(tagged)
#
#     # Extract all parts of speech from any text
#     chunker = RegexpParser("""
#                            NP: {<DT>?<JJ>*<NN>}    #To extract Noun Phrases
#                            P: {<IN>}               #To extract Prepositions
#                            V: {<V.*>}              #To extract Verbs
#                            PP: {<P> <NP>}          #To extract Prepostional Phrases
#                            VP: {<V> <NP|PP>*}      #To extarct Verb Phrases
#                            """)
#
#     # Print all parts of speech in above sentence
#     output = chunker.parse(tagged)
#     print("After Extracting\n", output)
#
#     # To draw the parse tree
#     output.draw()
    return 'hi'


if __name__ == '__main__':
    app.run(debug=True)
