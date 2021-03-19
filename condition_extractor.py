import re

class ConditionExtractor:
    
    def replaceConditions(self, sentence):
        sentence = sentence.replace('හෝ වැඩි', 'හෝවැඩි')
        sentence = sentence.replace('හෝ ඊට වැඩි', 'හෝවැඩි')
        sentence = sentence.replace('හෝ අඩු', 'හෝඅඩු')
        sentence = sentence.replace('හෝ ඊට අඩු', 'හෝඅඩු')
        return sentence

    def extractConditions(self, tags):
        # Extract Conditions
        min_, max_, condition_, conditions_ = 0, (len(tags) - 2), '', []
        while min_ < max_:
            if (tags[min_][1] == 'VP' or tags[min_][1] == 'NNC') and tags[(min_ + 1)][1] == 'NNC' and \
                    tags[(min_ + 2)][1] == 'JJ':
                condition_ = tags[min_][0] + ' ' + tags[(min_ + 1)][0] + ' ' + tags[(min_ + 2)][0]
                conditions_.append(condition_)
            elif (tags[min_][1] == 'VP' or tags[min_][1] == 'NNC') and tags[(min_ + 1)][1] == 'NNC' and \
                    tags[(min_ + 2)][1] == 'VP':
                condition_ = tags[min_][0] + ' ' + tags[(min_ + 1)][0] + ' ' + tags[(min_ + 2)][0]
                conditions_.append(condition_)
            elif (tags[min_][1] == 'VP' or tags[min_][1] == 'NNC') and tags[(min_ + 1)][1] == 'NUM' and \
                    tags[(min_ + 2)][1] == 'JJ':
                condition_ = tags[min_][0] + ' ' + tags[(min_ + 1)][0] + ' ' + tags[(min_ + 2)][0]
                conditions_.append(condition_)
            elif (tags[min_][1] == 'VP' or tags[min_][1] == 'NNC') and tags[(min_ + 1)][1] == 'NUM' and \
                    tags[(min_ + 2)][1] == 'VP':
                condition_ = tags[min_][0] + ' ' + tags[(min_ + 1)][0] + ' ' + tags[(min_ + 2)][0]
                conditions_.append(condition_)
            min_ += 1
        return conditions_

    def ho_wedi_issue(self, list_):
        min_ = 0
        while min_ < len(list_):
            j = list(list_[min_])
            if j[0] == 'හෝවැඩි':
                j[1] = 'JJ'
            list_[min_] = tuple(j)
            min_ += 1
        return list_

    def num_k_issue(self, sentence):
        nums_ = [int(s) for s in re.findall(r'\b\d+\b', sentence)]
        for num in nums_:
            x = str(num) + 'ක්'
            sentence = sentence.replace(str(num), x)
        return sentence
