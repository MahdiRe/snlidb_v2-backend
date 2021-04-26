from service.syntax_analysis import SyntaxAnalysis
from service.semantic_analysis import SemanticAnalysis
from repository.student_repo import StudentRepo

studentRepo = StudentRepo()


class SQLBuilder:

    def __init__(self, nlq):
        self.syntax_analysis = SyntaxAnalysis()
        self.semantic_analysis = SemanticAnalysis()

        self.__user_nlq = nlq
        self.__nlq = self.semantic_analysis.replace_conditions(self.__user_nlq)
        self.__tags = []
        self.__command = ''
        self.__table = ''
        self.__columns = []
        self.__logics = []
        self.__comparisons = []
        self.__conditions = []
        self.__updates = []
        self.__inserts = []
        self.__columns_ = ''
        self.__conditions_ = ''
        self.__updates_ = ''
        self.__insert_ = ''
        self.__sql_ = ''

    def __pos_tagging(self):
        self.__tags = (self.syntax_analysis.pos_tagger(self.__nlq))[0]
        return self.__tags

    def __lexicon_analysis(self):  # 1
        min_ = 0
        while min_ < len(self.__tags):
            query = "SELECT english_word,semantic_meaning FROM word_mappings" \
                    " WHERE sinhala_word='" + self.__tags[min_][0] + "' OR root_word='" + self.__tags[min_][0] + "';"
            result = studentRepo.execute_query(query)
            if result:
                for res in result:
                    if res[1] == 'neglect':
                        self.__tags[min_] = listToTuple(self.__tags[min_], res)
                    elif res[1] == 'command':
                        self.__command = res[0]
                        self.__tags[min_] = listToTuple(self.__tags[min_], res)
                    elif res[1] == 'table':
                        self.__table = res[0]
                        self.__tags[min_] = listToTuple(self.__tags[min_], res)
                    elif res[1] == 'column':
                        self.__columns.append(res[0])
                        self.__tags[min_] = listToTuple(self.__tags[min_], res)
                    elif res[1] == 'logic':
                        self.__logics.append(res[0])
                        self.__tags[min_] = listToTuple(self.__tags[min_], res)
                    elif res[1] == 'comparison':
                        self.__comparisons.append(res[0])
                        self.__tags[min_] = listToTuple(self.__tags[min_], res)
            else:
                self.__tags[min_] = listToTuple(self.__tags[min_], ('TBC', 'TBC'))
            min_ += 1

    def __derive_conditions(self):  # 2
        self.__conditions = self.semantic_analysis.extract_condition(self.__tags)
        return self.__conditions

    def __derive_updates(self):  # 3
        self.__updates = self.semantic_analysis.extract_updates(self.__tags)
        return self.__updates

    def __derive_inserts(self):  # 3
        self.__inserts = self.semantic_analysis.extract_inserts(self.__tags)
        return self.__inserts

    def __refine_columns(self):
        #  to remove columns that belongs to conditions
        for con in self.__conditions:
            for con1 in con:
                if con1[2] == 'column':
                    if self.__columns.count(con1[3]):
                        self.__columns.remove(con1[3])

        #  Solve 'siyaluma' issue
        # if (self.__columns.count('*')) and (len(self.__columns) != 1):
        #     self.__columns.remove('*')

    def __reserve_sql_words(self):
        if not self.__table:
            self.__table = 'student'

        if self.__table:
            # table found
            if self.__command:
                # command found
                if self.__command == 'SELECT':  # IF it is SELECT query
                    if self.__columns:
                        for col in self.__columns:  # Have specified columns?
                            self.__columns_ += col + ','
                        self.__columns_ = self.__columns_[:-1]  # Remove ','
                    else:  # No specified columns, then take all
                        self.__columns_ = '*'

                elif self.__command == 'UPDATE':
                    if self.__updates:
                        for update in self.__updates:  # Have specified updates?
                            self.__updates_ += update[0][3] + "=" + update[1][3] + ","
                        self.__updates_ = self.__updates_[:-1]  # Remove ','

                elif self.__command == 'INSERT':
                    if self.__inserts:
                        insert_bracket, insert_values = '(', '('
                        for insert in self.__inserts:  # Have specified updates?
                            insert_bracket += insert[0][3] + ','
                            insert_values += insert[1][3] + ','
                        insert_bracket = insert_bracket[:-1] + ')'  # Remove ','
                        insert_values = insert_values[:-1] + ')'  # Remove ','
                        self.__insert_ = "INSERT INTO " + self.__table + insert_bracket + " VALUES " + insert_values

                if self.__conditions:  # Have condition?
                    self.__conditions_ += 'WHERE '
                    min_ = 0
                    while min_ < len(self.__conditions):
                        self.__conditions_ += self.__conditions[min_][0][3] + self.__conditions[min_][1][3] + \
                                            self.__conditions[min_][2][3]
                        if (len(self.__conditions) > 1) and self.__logics and min_ < len(self.__logics):  # Have logics?
                            self.__conditions_ += " " + self.__logics[min_] + " "
                        min_ += 1
            else:
                print('Error: No command found!')
        else:
            print('Error: No table found!')

    def __arrange_sql_words(self):
        if self.__command == 'SELECT':
            self.__sql_ = self.__command + " " + self.__columns_ + " FROM " + self.__table
        elif self.__command == 'UPDATE':
            self.__sql_ = self.__command + " " + self.__table + " SET " + self.__updates_
        elif self.__command == 'DELETE':
            self.__sql_ = self.__command + " FROM " + self.__table
        elif self.__command == 'INSERT':
            self.__sql_ = self.__insert_
        if self.__conditions_:
            self.__sql_ += " " + self.__conditions_
        self.__sql_ += ';'
        return self.__sql_

    def nlq2sql_converter(self):
        self.__pos_tagging()
        self.__lexicon_analysis()
        if self.__command != 'INSERT':
            self.__derive_conditions()
        if self.__command == 'UPDATE':
            self.__derive_updates()
        if self.__command == 'INSERT':
            self.__derive_inserts()
        self.__refine_columns()
        self.__reserve_sql_words()
        self.__arrange_sql_words()
        return self.__sql_

    def get_sql(self):
        return self.__sql_

    def to_string(self):
        return 'tags : ' + str(self.__tags) + '\n' \
            'tables : ' + str(self.__table) + '\n' \
            'columns : ' + str(self.__columns) + '\n' \
            'conditions : ' + str(self.__conditions) + '\n' \
            'comparisons : ' + str(self.__comparisons) + '\n' \
            'logics : ' + str(self.__logics) + '\n' \
            'updates : ' + str(self.__updates) + '\n' \
            'inserts : ' + str(self.__inserts) + '\n' \
            'columns_ : ' + str(self.__columns_) + '\n' \
            'conditions_ : ' + str(self.__conditions_) + '\n' \
            'updates_ : ' + str(self.__updates_) + '\n' \
            'sql_ : ' + str(self.__sql_)


def listToTuple(tuple_, result_):
    j = list(tuple_)
    j.append(result_[1])
    j.append(result_[0])
    return tuple(j)
