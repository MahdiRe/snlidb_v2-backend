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
t8 = "ලකුනු 75 හෝ ඊට වැඩි සිසුන්ගේ විස්තර ලබාදෙන්න"


@app.route('/')
def hello_world():

    # nlq = t1
    # nlq = nlq.replace('හෝ වැඩි', 'හෝවැඩි')
    # nlq = nlq.replace('හෝ ඊට වැඩි', 'හෝවැඩි')
    # nlq = nlq.replace('හෝ අඩු', 'හෝඅඩු')
    # nlq = nlq.replace('හෝ ඊට අඩු', 'හෝඅඩු')

    nlq = condition_ex.replaceConditions(t8)
    nlq = condition_ex.num_k_issue(nlq)
    print('nlq: ' + nlq)


    # Tokenization + Stemming + POS Tagging
    tags = (tokenizer.posTagger(nlq))[0]
    tags = condition_ex.ho_wedi_issue(tags)
    print('tokens: ' + str(tags))

    conditions_ = condition_ex.extractConditions(tags)
    print('conditions: ' + str(conditions_))
    # # Extract Conditions
    # min_, max_, condition_, conditions_ = 0, (len(tags)-2), '', []
    # while min_ < max_:
    #     if (tags[min_][1] == 'VP' or tags[min_][1] == 'NNC') and tags[(min_+1)][1] == 'NNC' and tags[(min_+2)][1] == 'JJ':
    #         condition_ = tags[min_][0] + ' ' + tags[(min_+1)][0] + ' ' + tags[(min_+2)][0]
    #         conditions_.append(condition_)
    #     elif (tags[min_][1] == 'VP' or tags[min_][1] == 'NNC') and tags[(min_+1)][1] == 'NNC' and tags[(min_+2)][1] == 'VP':
    #         condition_ = tags[min_][0] + ' ' + tags[(min_+1)][0] + ' ' + tags[(min_+2)][0]
    #         conditions_.append(condition_)
    #     elif (tags[min_][1] == 'VP' or tags[min_][1] == 'NNC') and tags[(min_+1)][1] == 'NUM' and tags[(min_+2)][1] == 'JJ':
    #         condition_ = tags[min_][0] + ' ' + tags[(min_+1)][0] + ' ' + tags[(min_+2)][0]
    #         conditions_.append(condition_)
    #     elif (tags[min_][1] == 'VP' or tags[min_][1] == 'NNC') and tags[(min_ + 1)][1] == 'NUM' and tags[(min_ + 2)][1] == 'VP':
    #         condition_ = tags[min_][0] + ' ' + tags[(min_ + 1)][0] + ' ' + tags[(min_ + 2)][0]
    #         conditions_.append(condition_)
    #
    #     min_ += 1

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
    # command, table, columns, logics, conditions = '', '', [], [], []
    # for tag in tags:
    #     query = "SELECT english_word,semantic_meaning FROM word_mappings WHERE sinhala_word='"+tag[0] + \
    #             "' OR root_word='" + tag[0] + "';"
    #     result = db.executeQuery(query)
    #     for i in result:
    #         if i[1] != 'neglect':
    #             if i[1] == 'command':
    #                 command = i[0]
    #             elif i[1] == 'table':
    #                 table = i[0]
    #             elif i[1] == 'column':
    #                 columns.append((tag[0], i[0]))
    #             elif i[1] == 'logic':
    #                 logics.append((tag[0], i[0]))
    #             elif i[1] == 'condition':
    #                 conditions.append((tag[0], i[0]))

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
    return str(conditions_)


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
    return str(tokenizer.posTagger(t7))

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
