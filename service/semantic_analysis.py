from repository.student_repo import StudentRepo

studentRepo = StudentRepo()


class SemanticAnalysis:

    def extract_condition(self, tags):
        # Extract Conditions
        min_, max_, conditions_ = 0, (len(tags) - 2), []
        while min_ < max_:
            # Example: ලකුනු 75ට වැඩි, නම සුනිල්ට සමාන, වයස 14 වන
            if (tags[min_][2] == 'column') and \
                    self.compare_or(tags[(min_ + 1)][1], 'NNC', 'NUM', 'NNP', 'NCV') and \
                    (tags[(min_ + 2)][2] == 'comparison' or (tags[(min_ + 2)][1] == 'VP' and tags[(min_ + 2)][2] != 'column')):
                tags[(min_ + 1)] = self.__change_specific_tuple_value(tags[(min_ + 1)], 3,
                                                self.__replace_last_character(tags[(min_ + 1)][0]))
                if tags[(min_ + 2)][2] == 'comparison':
                    conditions_.append([tags[min_], tags[(min_ + 2)], tags[(min_ + 1)]])
                else:
                    # Any queries without comparisons - Ex: වයස 14 වන
                    tags[(min_ + 2)] = self.__change_specific_tuple_value(tags[(min_ + 2)], 3, "=")
                    conditions_.append([tags[min_], tags[(min_ + 2)], tags[(min_ + 1)]])

            # Example: 75ට සමාන ලකුනු, සුනිල්ට සමාන නම
            elif (self.compare_or(tags[min_][1], 'NNC', 'NUM', 'NNP', 'NCV')) and \
                    tags[(min_ + 1)][2] == 'comparison' and \
                    (tags[(min_ + 2)][2] == 'column'):
                tags[min_] = self.__change_specific_tuple_value(tags[min_], 3,
                                                 self.__replace_last_character(tags[min_][0]))
                conditions_.append([tags[(min_ + 2)], tags[(min_ + 1)], tags[min_]])
            min_ += 1

        #  Example: කමල්ගේ, නිමල්ගේ, සුනිල්ගේ
        min_, max_ = 0, (len(tags) - 1)
        if len(conditions_) == 0:
            while min_ < max_:
                if tags[min_][1] == 'NNP' and tags[min_][2] == 'TBC' and tags[min_+1][1] != 'POST':  # Avoid updates
                    tag = self.__change_specific_tuple_value(tags[min_], 3, self.__replace_last_character(tags[min_][0]))
                    conditions_.append([('-', '-', 'column', 'name'), ('-', '-', 'comparison', '='), tag])
                min_ += 1
        return conditions_

    def extract_updates(self, tags):
        # Extract Updates
        min_, max_, updates_ = 0, (len(tags) - 2), []
        while min_ < max_:

            # Example: නම සුනිල් ලෙස, වයස 45 ලෙස, ලකුනු 50 ලෙස
            if (tags[min_][2] == 'column') and \
                    (self.compare_or(tags[(min_ + 1)][1], 'NNC', 'NUM', 'NNP', 'NCV')) and \
                    tags[(min_ + 2)][1] == 'POST':  # POST
                tags[(min_ + 1)] = self.__change_specific_tuple_value(tags[(min_ + 1)], 3,
                                                self.__replace_last_character(tags[(min_ + 1)][0]))
                updates_.append([tags[min_], tags[(min_ + 1)]])
            min_ += 1
        return updates_

    def extract_inserts(self, tags):
        # Extract Inserts
        min_, max_, inserts_ = 0, (len(tags) - 2), []
        while min_ < max_:

            # Example: නම සුනිල් ලෙස, වයස 45 ලෙස, ලකුනු 50 ලෙස
            if (tags[min_][2] == 'column') and \
                    (self.compare_or(tags[(min_ + 1)][1], 'NNC', 'NUM', 'NNP', 'NCV')) and \
                    tags[(min_ + 2)][1] == 'VP':
                tags[(min_ + 1)] = self.__change_specific_tuple_value(tags[(min_ + 1)], 3,
                                                self.__replace_last_character(tags[(min_ + 1)][0]))
                inserts_.append([tags[min_], tags[(min_ + 1)]])
            min_ += 1
        return inserts_

    def replace_conditions(self, sentence):
        sentence = sentence.replace('අඩුවෙන්', 'අඩු')
        sentence = sentence.replace('වැඩියෙන්', 'වැඩි')
        sentence = sentence.replace('හෝ වැඩි', 'හෝවැඩි')
        sentence = sentence.replace('හෝ ඊට වැඩි', 'හෝවැඩි')
        sentence = sentence.replace('හෝ අඩු', 'හෝඅඩු')
        sentence = sentence.replace('හෝ ඊට අඩු', 'හෝඅඩු')
        return sentence

    def __replace_last_character(self, word):
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

    def __change_specific_tuple_value(self, tuple_, index, value):
        list_ = list(tuple_)
        list_[index] = value
        tuple_ = tuple(list_)
        return tuple_

    def compare_or(self, value, equal1, equal2, equal3, equal4):
        return value == equal1 or value == equal2 or value == equal3 or value == equal4



# ----------------------
# (VP or NNC) + NNC + JJ
# (VP or NNC) + NNC + VP
# (VP or NNC) + NUM + JJ
# (VP or NNC) + NUM + VP
# ----------------------
# (VP or NNC) -> [1] is column & [3] is comparison
# ----------------------
