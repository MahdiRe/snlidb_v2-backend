from db import Db


class ConditionExtractor:

    def __init__(self, db):
        self.db = db

    def extractCondition2(self, tags):
        # Extract Conditions
        min_, max_, conditions_ = 0, (len(tags) - 2), []
        while min_ < max_:
            # Example: ලකුනු 75ට වැඩි, නම සුනිල්ට සමාන
            if tags[min_][2] == 'column' and \
                    (tags[(min_ + 1)][1] == 'NNC' or tags[(min_ + 1)][1] == 'NUM' or tags[(min_ + 1)][1] == 'NNP') and \
                    tags[(min_ + 2)][2] == 'comparison':
                tags[(min_ + 1)] = self.changeSpecificTupleValue(tags[(min_ + 1)], 3,
                                                                 self.replaceLastCharacter(tags[(min_ + 1)][0]))
                conditions_.append([tags[min_], tags[(min_ + 2)], tags[(min_ + 1)]])

            # Example: 75ට සමාන ලකුනු, සුනිල්ට සමාන නම
            elif (tags[min_][1] == 'NNC' or tags[min_][1] == 'NUM' or tags[min_][1] == 'NNP') and \
                    tags[(min_ + 1)][2] == 'comparison' and \
                    tags[(min_ + 2)][2] == 'column':
                tags[min_] = self.changeSpecificTupleValue(tags[min_], 3,
                                                           self.replaceLastCharacter(tags[min_][0]))
                conditions_.append([tags[(min_ + 2)], tags[(min_ + 1)], tags[min_]])
                print(conditions_)

            min_ += 1

        if len(conditions_) == 0:
            for tag in tags:
                if tag[1] == 'NNP':
                    tag = self.changeSpecificTupleValue(tag, 3, self.replaceLastCharacter(tag[0]))
                    sql_ = "SELECT * FROM student WHERE name = " + tag[3]
                    result = self.db.executeQuery(sql_)
                    if result:
                        print('wait')
                        conditions_.append([('-', '-', 'column', 'name'), ('-', '-', 'comparison', '='), tag])
                    else:
                        print('Error: No ' + tag[3] + 'found!')

        return conditions_

    def replaceConditions(self, sentence):
        sentence = sentence.replace('අඩුවෙන්', 'අඩු')
        sentence = sentence.replace('වැඩියෙන්', 'වැඩි')
        sentence = sentence.replace('හෝ වැඩි', 'හෝවැඩි')
        sentence = sentence.replace('හෝ ඊට වැඩි', 'හෝවැඩි')
        sentence = sentence.replace('හෝ අඩු', 'හෝඅඩු')
        sentence = sentence.replace('හෝ ඊට අඩු', 'හෝඅඩු')
        return sentence

    def replaceLastCharacter(self, word):
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
        return "'" + word + "'"

    def changeSpecificTupleValue(self, tuple_, index, value):
        list_ = list(tuple_)
        list_[index] = value
        tuple_ = tuple(list_)
        return tuple_

    # def extractConditions(self, tags):
    #     # Extract Conditions
    #     min_, max_, condition_, conditions_ = 0, (len(tags) - 2), '', []
    #     while min_ < max_:
    #         if (tags[min_][1] == 'VP' or tags[min_][1] == 'NNC') and tags[(min_ + 1)][1] == 'NNC' and \
    #                 tags[(min_ + 2)][1] == 'JJ':
    #             condition_ = tags[min_][0] + ' ' + tags[(min_ + 1)][0] + ' ' + tags[(min_ + 2)][0]
    #             conditions_.append(condition_)
    #         elif (tags[min_][1] == 'VP' or tags[min_][1] == 'NNC') and tags[(min_ + 1)][1] == 'NNC' and \
    #                 tags[(min_ + 2)][1] == 'VP':
    #             condition_ = tags[min_][0] + ' ' + tags[(min_ + 1)][0] + ' ' + tags[(min_ + 2)][0]
    #             conditions_.append(condition_)
    #         elif (tags[min_][1] == 'VP' or tags[min_][1] == 'NNC') and tags[(min_ + 1)][1] == 'NUM' and \
    #                 tags[(min_ + 2)][1] == 'JJ':
    #             condition_ = tags[min_][0] + ' ' + tags[(min_ + 1)][0] + ' ' + tags[(min_ + 2)][0]
    #             conditions_.append(condition_)
    #         elif (tags[min_][1] == 'VP' or tags[min_][1] == 'NNC') and tags[(min_ + 1)][1] == 'NUM' and \
    #                 tags[(min_ + 2)][1] == 'VP':
    #             condition_ = tags[min_][0] + ' ' + tags[(min_ + 1)][0] + ' ' + tags[(min_ + 2)][0]
    #             conditions_.append(condition_)
    #         min_ += 1
    #     return conditions_

    # def extractCondition1(self, tags):
    #     # Extract Conditions
    #     min_, max_, condition_, conditions_ = 0, (len(tags) - 2), '', []
    #     while min_ < max_:
    #         if (tags[min_][1] == 'VP' or tags[min_][1] == 'NNC') and \
    #                 (tags[(min_ + 1)][1] == 'NNC' or tags[(min_ + 1)][1] == 'NUM') and \
    #                 (tags[(min_ + 2)][1] == 'JJ' or tags[(min_ + 2)][1] == 'VP'):
    #             if tags[min_][2] == 'column' and tags[(min_ + 2)][2] == 'comparison':
    #                 condition_ = tags[min_][0] + ' ' + tags[(min_ + 1)][0] + ' ' + tags[(min_ + 2)][0]
    #                 conditions_.append([tags[min_], tags[(min_ + 1)], tags[(min_ + 2)]])
    #         min_ += 1
    #     return conditions_

    # def ho_wedi_JJ_issue(self, list_):
    #     min_ = 0
    #     while min_ < len(list_):
    #         j = list(list_[min_])
    #         if j[0] == 'හෝවැඩි':
    #             j[1] = 'JJ'
    #         list_[min_] = tuple(j)
    #         min_ += 1
    #     return list_

    # def num_k_issue(self, sentence):
    #     nums_ = [int(s) for s in re.findall(r'\b\d+\b', sentence)]
    #     for num in nums_:
    #         x = str(num) + 'ක්'
    #         sentence = sentence.replace(str(num), x)
    #     return sentence

    # def num_issue(self, list_):
    #     min_ = 0
    #     while min_ < len(list_):
    #         if any(char.isdigit() for char in list_[min_]):
    #             list_[min_] = list_[min_].replace('ක්', '')
    #             list_[min_] = list_[min_].replace('ක', '')
    #             list_[min_] = list_[min_].replace('ත්', '')
    #             list_[min_] = list_[min_].replace('වූ', '')
    #             list_[min_] = list_[min_].replace('වු', '')
    #             list_[min_] = list_[min_].replace('ට', '')
    #         min_ += 1
    #     return list_
