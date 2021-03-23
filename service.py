from db import Db
from tokenization import Tokenization
from condition_extractor import ConditionExtractor


class Service:

    def __init__(self, app):
        self.db = Db(app)
        self.condition_ex = ConditionExtractor()
        self.tokenizer = Tokenization()

    def generateSQL(self, query):

        nlq = self.condition_ex.replaceConditions(query)
        print('nlq: ' + nlq)

        # Tokenization + Stemming + POS Tagging
        tags = (self.tokenizer.posTagger(nlq))[0]
        print('tokens: ' + str(tags))

        # Derive the Command, Table, Columns, Logics and Conditions
        command, table, columns, logics, comparisons, min_ = '', '', [], [], [], 0

        while min_ < len(tags):
            query = "SELECT english_word,semantic_meaning FROM word_mappings" \
                    " WHERE sinhala_word='" + tags[min_][0] + "' OR root_word='" + tags[min_][0] + "';"
            result = self.db.executeQuery(query)
            if result:
                # print(result)
                for res in result:
                    if res[1] == 'neglect':
                        tags[min_] = self.listToTuple(tags[min_], res)
                    elif res[1] == 'command':
                        command = res[0]
                        tags[min_] = self.listToTuple(tags[min_], res)
                    elif res[1] == 'table':
                        table = res[0]
                        tags[min_] = self.listToTuple(tags[min_], res)
                    elif res[1] == 'column':
                        # columns.append((tags[min_][0], res[0]))
                        columns.append(res[0])
                        tags[min_] = self.listToTuple(tags[min_], res)
                    elif res[1] == 'logic':
                        # logics.append((tags[min_][0], res[0]))
                        logics.append(res[0])
                        tags[min_] = self.listToTuple(tags[min_], res)
                    elif res[1] == 'comparison':
                        # conditions.append((tags[min_][0], res[0]))
                        comparisons.append(res[0])
                        tags[min_] = self.listToTuple(tags[min_], res)
            else:
                tags[min_] = self.listToTuple(tags[min_], ('TBC', 'TBC'))
            min_ += 1

        conditions = self.condition_ex.extractCondition2(tags)

        # What I have now?
        x = 'tags : ' + str(tags) + '\n' \
            'tables : ' + str(table) + '\n' \
            'columns : ' + str(columns) + '\n' \
            'conditions : ' + str(conditions) + '\n' \
            'logics : ' + str(logics)
        print(x)

        # Remove columns that involve in conditions.
        for con in conditions:
            for con1 in con:
                if con1[2] == 'column':
                    columns.remove(con1[3])

        sql_, columns_, conditions_ = '', '', ''

        if table:
            # table found
            if command:
                # command found
                if command == 'SELECT':  # IF it is SELECT query
                    if columns:
                        for col in columns:  # Have specified columns?
                            columns_ += col + ','
                        columns_ = columns_[:-1]  # Remove ','
                    else:  # No specified columns, then take all
                        columns_ = '*'

                    if conditions:  # Have condition?
                        conditions_ += 'WHERE '
                        min_ = 0
                        while min_ < len(conditions):
                            print(conditions[min_])
                            conditions_ += conditions[min_][0][3] + conditions[min_][2][3] + conditions[min_][1][0]
                            if logics and min_ < len(logics):  # Have logics?
                                conditions_ += " " + logics[min_] + " "
                            min_ += 1
            else:
                print('Error: No command found!')
        else:
            print('Error: No table found!')

        # What I have now?
        x = 'command: ' + command + '\tcolumns: ' + columns_ + '\ttable: ' + table + '\tconditions: ' + conditions_

        # Generate SQL query
        sql_ = command + " " + columns_ + " FROM " + table + " " + conditions_ + ";"

        return sql_

    def listToTuple(self, tuple_, result_):
        j = list(tuple_)
        j.append(result_[1])
        j.append(result_[0])
        return tuple(j)


