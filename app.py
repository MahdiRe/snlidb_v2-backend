from flask import Flask, request
from flask_cors import CORS
from tokenization import Tokenization
from translation import Translation
from stemming import Stemming
from condition_extractor import ConditionExtractor
from db import Db
# import nltk
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
from nltk import pos_tag, word_tokenize, RegexpParser

app = Flask(__name__)
CORS(app)
db = Db(app)
condition_ex = ConditionExtractor()
tokenizer = Tokenization()
translator = Translation(app)

# test = 'සියලුම සිසුන්ගේ තොරතුරු ලබා දෙන්න'
# test1 = 'ලකුනු 75ට සමාන වැඩි සිසුන්ගේ නම් නම සුනිල් දත්ත තොරතුරු හෝඅඩු'
t1 = "සියලුම සිසුන්ගේ තොරතුරු ලබාදෙන්න"
t2 = "සියලුම සිසුන්ගේ නම ලබාදෙන්න"
t3 = "සුනිල්ගේ විස්තර ලබාදෙන්න"
t51 = "ලකුනු 75ට වැඩි සිසුන්ගේ විස්තර ලබාදෙන්න ලකුනු 75ක් ගත් වයස 14 වු ලකුනු 75ක් හෝඅඩු ලබාදෙන්න"
t4 = "ලකුනු 75ට වැඩි සිසුන්ගේ විස්තර ලබාදෙන්න"
t5 = "ලකුනු 75ක් ගත් සිසුන්ගේ විස්තර ලබාදෙන්න"
t6 = "වයස 14 වු  සිසුන්ගේ විස්තර ලබාදෙන්න"
t7 = "ලකුනු 75ක් හෝඅඩු සිසුන්ගේ විස්තර ලබාදෙන්න"
t77 = "ලකුනු 75 හෝඅඩු සිසුන්ගේ විස්තර ලබාදෙන්න"
t8 = "ලකුනු 75 හෝ ඊට වැඩි සිසුන්ගේ විස්තර ලබාදෙන්න"
t9 = "ලකුනු 75ක් හෝවැඩි සිසුන්ගේ විස්තර ලබාදෙන්න"
t10 = "ලකුනු 75 හෝවැඩි සිසුන්ගේ විස්තර ලබාදෙන්න"


@app.route('/')
def hello_world():

    nlq = condition_ex.replaceConditions(t8)
    # nlq = condition_ex.num_k_issue(nlq)
    print('nlq: ' + nlq)

    # Tokenization + Stemming + POS Tagging
    tags = (tokenizer.posTagger(nlq))[0]
    # tags = condition_ex.ho_wedi_issue(tags)
    print('tokens: ' + str(tags))

    # conditions_ = condition_ex.extractConditions(tags)
    # print('conditions: ' + str(conditions_))

    # chunker = RegexpParser("""
    #                             COND: {<VP> <NNC> <JJ>}
    #                             COND: {<VP> <NNC> <VP>}
    #                             COND: {<NNC> <NUM> <VP>}
    #                             COND: {<VP> <NNC> <JJ>}
    #                         """)

    # # Print all parts of speech in above sentence
    # output = chunker.parse(tags[0])
    # print("After Extracting\n", output)
    #
    # # To draw the parse tree
    # output.draw()

    # Derive the Command, Table, Columns, Logics and Conditions

    # Derive the operation
    command, table, columns, logics, conditions, min_ = '', '', [], [], [], 0
    # print(str(tags))

    while min_ < len(tags):
        query = "SELECT english_word,semantic_meaning FROM word_mappings" \
                " WHERE sinhala_word='"+tags[min_][0] + "' OR root_word='" + tags[min_][0] + "';"
        result = db.executeQuery(query)
        if result:
            # print(result)
            for res in result:
                if res[1] == 'neglect':
                    tags[min_] = listToTuple(tags[min_], res)
                elif res[1] == 'command':
                    command = res[0]
                    tags[min_] = listToTuple(tags[min_], res)
                elif res[1] == 'table':
                    table = res[0]
                    tags[min_] = listToTuple(tags[min_], res)
                elif res[1] == 'column':
                    columns.append((tags[min_][0], res[0]))
                    tags[min_] = listToTuple(tags[min_], res)
                elif res[1] == 'logic':
                    logics.append((tags[min_][0], res[0]))
                    tags[min_] = listToTuple(tags[min_], res)
                elif res[1] == 'comparison':
                    conditions.append((tags[min_][0], res[0]))
                    tags[min_] = listToTuple(tags[min_], res)
        else:
            tags[min_] = listToTuple(tags[min_], ('TBC', 'TBC'))
        min_ += 1

    con_ex = condition_ex.extractCondition2(tags)

    # Replace the logics
    # print('columns' + str(columns))
    # print('logics' + str(logics))
    # print('conditions' + str(conditions))

    # conditional_word = ''
    # for con in conditions:
    #     print(con)
    #     conditional_word = t7.replace(con[0], con[1])
    #
    # conditional_tags = tokenizer.posTagger(conditional_word)
    #
    # # ab = command + ' ' + str(columns) + ' FROM ' + table
    # return str(conditional_tags)
    return str(con_ex)


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

def listToTuple(tuple_, result_):
    j = list(tuple_)
    j.append(result_[1])
    j.append(result_[0])
    return tuple(j)

@app.route('/a')
def a():
    print(str(tokenizer.posTagger(t4)))
    print(str(tokenizer.posTagger(t5)))
    print(str(tokenizer.posTagger(t6)))
    print(str(tokenizer.posTagger(t7)))
    print(str(tokenizer.posTagger(t77)))
    print(str(tokenizer.posTagger(t9)))
    print(str(tokenizer.posTagger(t10)))
    return str(tokenizer.posTagger(t9))

@app.route('/b')
def b():
    # Example text
    sample_text = "The quick brown fox jumps over the lazy dog"

    # Find all parts of speech in above sentence
    tagged = pos_tag(word_tokenize(sample_text))

    print(tagged)

    # Extract all parts of speech from any text
    chunker = RegexpParser(""" 
                           NP: {<DT>?<JJ>*<NN>}    #To extract Noun Phrases 
                           P: {<IN>}               #To extract Prepositions 
                           V: {<V.*>}              #To extract Verbs 
                           PP: {<P> <NP>}          #To extract Prepostional Phrases 
                           VP: {<V> <NP|PP>*}      #To extarct Verb Phrases 
                           """)

    # Print all parts of speech in above sentence
    output = chunker.parse(tagged)
    print("After Extracting\n", output)

    # To draw the parse tree
    output.draw()
    return 'hi'


if __name__ == '__main__':
    app.run(debug=True)
