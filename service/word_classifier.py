from repository.student_repo import StudentRepo

studentRepo = StudentRepo()


class WordClassifier:
    @staticmethod
    def extractCondition(tags):
        # Extract Conditions
        min_, max_, conditions_ = 0, (len(tags) - 2), []
        while min_ < max_:
            # Example: ලකුනු 75ට වැඩි, නම සුනිල්ට සමාන
            if tags[min_][2] == 'column' and \
                    (tags[(min_ + 1)][1] == 'NNC' or tags[(min_ + 1)][1] == 'NUM' or tags[(min_ + 1)][1] == 'NNP') and \
                    tags[(min_ + 2)][2] == 'comparison':
                tags[(min_ + 1)] = WordClassifier.changeSpecificTupleValue(tags[(min_ + 1)], 3,
                                                                           WordClassifier.replaceLastCharacter(
                                                                               tags[(min_ + 1)][0]))
                conditions_.append([tags[min_], tags[(min_ + 2)], tags[(min_ + 1)]])

            # Example: 75ට සමාන ලකුනු, සුනිල්ට සමාන නම
            elif (tags[min_][1] == 'NNC' or tags[min_][1] == 'NUM' or tags[min_][1] == 'NNP') and \
                    tags[(min_ + 1)][2] == 'comparison' and \
                    tags[(min_ + 2)][2] == 'column':
                tags[min_] = WordClassifier.changeSpecificTupleValue(tags[min_], 3,
                                                                     WordClassifier.replaceLastCharacter(tags[min_][0]))
                conditions_.append([tags[(min_ + 2)], tags[(min_ + 1)], tags[min_]])
                # print(conditions_)

            min_ += 1

        if len(conditions_) == 0:
            for tag in tags:
                if tag[1] == 'NNP':
                    tag = WordClassifier.changeSpecificTupleValue(tag, 3, WordClassifier.replaceLastCharacter(tag[0]))
                    sql_ = "SELECT * FROM student WHERE name = " + tag[3]
                    result = studentRepo.executeQuery(sql_)
                    if result:
                        # print('wait')
                        conditions_.append([('-', '-', 'column', 'name'), ('-', '-', 'comparison', '='), tag])
                    else:
                        print('Error: No ' + tag[3] + 'found!')

        return conditions_

    @staticmethod
    def extractUpdates(tags):
        # Extract Conditions
        min_, max_, conditions_ = 0, (len(tags) - 2), []
        while min_ < max_:
            # Example: නම සුනිල් ලෙස, වයස 45 ලෙස, ලකුනු 50 ලෙස
            if tags[min_][2] == 'column' and \
                    (tags[(min_ + 1)][1] == 'NNC' or tags[(min_ + 1)][1] == 'NUM' or tags[(min_ + 1)][1] == 'NNP') and \
                    tags[(min_ + 2)][2] != 'comparison':
                tags[(min_ + 1)] = WordClassifier.changeSpecificTupleValue(tags[(min_ + 1)], 3,
                                                                           WordClassifier.replaceLastCharacter(
                                                                               tags[(min_ + 1)][0]))
                conditions_.append([tags[min_], tags[(min_ + 1)]])
            min_ += 1
        return conditions_

    @staticmethod
    def replaceConditions(sentence):
        sentence = sentence.replace('අඩුවෙන්', 'අඩු')
        sentence = sentence.replace('වැඩියෙන්', 'වැඩි')
        sentence = sentence.replace('හෝ වැඩි', 'හෝවැඩි')
        sentence = sentence.replace('හෝ ඊට වැඩි', 'හෝවැඩි')
        sentence = sentence.replace('හෝ අඩු', 'හෝඅඩු')
        sentence = sentence.replace('හෝ ඊට අඩු', 'හෝඅඩු')
        return sentence

    @staticmethod
    def replaceLastCharacter(word):
        if any(char.isdigit() for char in word):
            if word[-1:] == 'ට':
                word = word.replace('ට', '')
            elif word[-1:] == 'ක':
                word = word.replace('ක', '')
            elif word[-2:] == 'ක්':
                word = word.replace('ක්', '')
            elif word[-2:] == 'ත්':
                word = word.replace('ත්', '')
            elif word[-2:] == 'වූ':
                word = word.replace('වූ', '')
            elif word[-2:] == 'වු':
                word = word.replace('වු', '')
        else:
            if word[-2:] == 'ගේ':
                word = word.replace('ගේ', '')
            elif word[-1:] == 'ට':
                word = word.replace('ට', '')
            word = "'" + word + "'"
        return word

    @staticmethod
    def changeSpecificTupleValue(tuple_, index, value):
        list_ = list(tuple_)
        list_[index] = value
        tuple_ = tuple(list_)
        return tuple_

# ----------------------
# (VP or NNC) + NNC + JJ
# (VP or NNC) + NNC + VP
# (VP or NNC) + NUM + JJ
# (VP or NNC) + NUM + VP
# ----------------------
# (VP or NNC) -> [1] is column & [3] is comparison
# ----------------------
