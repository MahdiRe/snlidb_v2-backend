from service.tokenization import Tokenization
from service.word_classifier import WordClassifier
from repository.student_repo import StudentRepo

tokenizer = Tokenization()
studentRepo = StudentRepo()


class SQLBuilder:

    def __init__(self, nlq):
        self.user_nlq = nlq
        self.nlq = WordClassifier.replaceConditions(self.user_nlq)
        self.tags = ()
        self.command = ''
        self.table = ''
        self.columns = []
        self.logics = []
        self.comparisons = []
        self.conditions = []
        self.updates = []
        self.columns_ = ''
        self.conditions_ = ''
        self.updates_ = ''
        self.sql_ = ''

    def pos_tagging(self):
        self.tags = (tokenizer.posTagger(self.nlq))[0]
        return self.tags

    def semantic_analysis(self):  # 1
        min_ = 0
        while min_ < len(self.tags):
            query = "SELECT english_word,semantic_meaning FROM word_mappings" \
                    " WHERE sinhala_word='" + self.tags[min_][0] + "' OR root_word='" + self.tags[min_][0] + "';"
            result = studentRepo.executeQuery(query)
            if result:
                for res in result:
                    if res[1] == 'neglect':
                        self.tags[min_] = listToTuple(self.tags[min_], res)
                    elif res[1] == 'command':
                        self.command = res[0]
                        self.tags[min_] = listToTuple(self.tags[min_], res)
                    elif res[1] == 'table':
                        self.table = res[0]
                        self.tags[min_] = listToTuple(self.tags[min_], res)
                    elif res[1] == 'column':
                        self.columns.append(res[0])
                        self.tags[min_] = listToTuple(self.tags[min_], res)
                    elif res[1] == 'logic':
                        self.logics.append(res[0])
                        self.tags[min_] = listToTuple(self.tags[min_], res)
                    elif res[1] == 'comparison':
                        self.comparisons.append(res[0])
                        self.tags[min_] = listToTuple(self.tags[min_], res)
            else:
                self.tags[min_] = listToTuple(self.tags[min_], ('TBC', 'TBC'))
            min_ += 1

    def derive_conditions(self):  # 2
        self.conditions = WordClassifier.extractCondition(self.tags)

    def derive_updates(self):  # 3
        self.updates = WordClassifier.extractUpdates(self.tags)

    def refine_columns(self):
        for con in self.conditions:
            for con1 in con:
                if con1[2] == 'column':
                    if self.columns.count(con1[3]):
                        self.columns.remove(con1[3])

    def reserve_sql_words(self):
        if not self.table:
            self.table = 'student'

        if self.table:
            # table found
            if self.command:
                # command found
                if self.command == 'SELECT':  # IF it is SELECT query
                    if self.columns:
                        for col in self.columns:  # Have specified columns?
                            self.columns_ += col + ','
                        self.columns_ = self.columns_[:-1]  # Remove ','
                    else:  # No specified columns, then take all
                        self.columns_ = '*'

                elif self.command == 'UPDATE':
                    if self.updates:
                        for update in self.updates:  # Have specified updates?

                            self.updates_ += update[0][3] + "=" + update[1][3] + ","
                        self.updates_ = self.updates_[:-1]  # Remove ','

                if self.conditions:  # Have condition?
                    self.conditions_ += 'WHERE '
                    min_ = 0
                    while min_ < len(self.conditions):
                        self.conditions_ += self.conditions[min_][0][3] + self.conditions[min_][1][3] + self.conditions[min_][2][3]
                        if self.logics and min_ < len(self.logics):  # Have logics?
                            self.conditions_ += " " + self.logics[min_] + " "
                        min_ += 1
            else:
                print('Error: No command found!')
        else:
            print('Error: No table found!')

    def arrange_sql_words(self):
        if self.command == 'SELECT':
            self.sql_ = self.command + " " + self.columns_ + " FROM " + self.table
        elif self.command == 'UPDATE':
            self.sql_ = self.command + " " + self.table + " SET " + self.updates_
        elif self.command == 'DELETE':
            self.sql_ = self.command + " FROM " + self.table
        if self.conditions_:
            self.sql_ += " " + self.conditions_
        self.sql_ += ';'


def listToTuple(tuple_, result_):
    j = list(tuple_)
    j.append(result_[1])
    j.append(result_[0])
    return tuple(j)
