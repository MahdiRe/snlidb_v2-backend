# from repository.student_repo import StudentRepo
# from service.tokenization import Tokenization
# from service.word_classifier import WordClassifier
#
# studentRepo = StudentRepo()
# wordClassifier = WordClassifier()
# tokenizer = Tokenization()
#
#
# class QueryGenerator:
#
#     @staticmethod
#     def generateSQL(query):
#
#         nlq = wordClassifier.replaceConditions(query)
#         print('nlq: ' + nlq)
#
#         # Tokenization + Stemming + POS Tagging
#         tags = (tokenizer.posTagger(nlq))[0]
#         print('tokens: ' + str(tags))
#
#         # Derive the Command, Table, Columns, Logics and Conditions
#         command, table, columns, logics, comparisons, min_ = '', '', [], [], [], 0
#
#         while min_ < len(tags):
#             query = "SELECT english_word,semantic_meaning FROM word_mappings" \
#                     " WHERE sinhala_word='" + tags[min_][0] + "' OR root_word='" + tags[min_][0] + "';"
#             result = studentRepo.executeQuery(query)
#             if result:
#                 # print(result)
#                 for res in result:
#                     if res[1] == 'neglect':
#                         tags[min_] = listToTuple(tags[min_], res)
#                     elif res[1] == 'command':
#                         command = res[0]
#                         tags[min_] = listToTuple(tags[min_], res)
#                     elif res[1] == 'table':
#                         table = res[0]
#                         tags[min_] = listToTuple(tags[min_], res)
#                     elif res[1] == 'column':
#                         # columns.append((tags[min_][0], res[0]))
#                         columns.append(res[0])
#                         tags[min_] = listToTuple(tags[min_], res)
#                     elif res[1] == 'logic':
#                         # logics.append((tags[min_][0], res[0]))
#                         logics.append(res[0])
#                         tags[min_] = listToTuple(tags[min_], res)
#                     elif res[1] == 'comparison':
#                         # conditions.append((tags[min_][0], res[0]))
#                         comparisons.append(res[0])
#                         tags[min_] = listToTuple(tags[min_], res)
#             else:
#                 tags[min_] = listToTuple(tags[min_], ('TBC', 'TBC'))
#             min_ += 1
#
#         # Derive the conditions
#         conditions = wordClassifier.extractCondition(tags)
#         updates = wordClassifier.extractUpdates(tags)
#
#         # Remove columns that involve in conditions.
#         for con in conditions:
#             for con1 in con:
#                 if con1[2] == 'column':
#                     if columns.count(con1[3]):
#                         columns.remove(con1[3])
#
#         # What I have now?
#         x = 'tags : ' + str(tags) + '\n' \
#             'tables : ' + str(table) + '\n' \
#             'columns : ' + str(columns) + '\n' \
#             'conditions : ' + str(conditions) + '\n' \
#             'logics : ' + str(logics) + '\n' \
#             'updates : ' + str(updates)
#         print(x)
#
#         sql_, columns_, conditions_, updates_ = '', '', '', ''
#
#         if not table:
#             table = 'student'
#
#         if table:
#             # table found
#             if command:
#                 # command found
#                 if command == 'SELECT':  # IF it is SELECT query
#                     if columns:
#                         for col in columns:  # Have specified columns?
#                             columns_ += col + ','
#                         columns_ = columns_[:-1]  # Remove ','
#                     else:  # No specified columns, then take all
#                         columns_ = '*'
#
#                 elif command == 'UPDATE':
#                     if updates:
#                         for update in updates:  # Have specified updates?
#
#                             updates_ += update[0][3] + "=" + update[1][3] + ","
#                         updates_ = updates_[:-1]  # Remove ','
#
#                 if conditions:  # Have condition?
#                     conditions_ += 'WHERE '
#                     min_ = 0
#                     while min_ < len(conditions):
#                         # print(conditions[min_])
#                         conditions_ += conditions[min_][0][3] + conditions[min_][1][3] + conditions[min_][2][3]
#                         if logics and min_ < len(logics):  # Have logics?
#                             conditions_ += " " + logics[min_] + " "
#                         min_ += 1
#             else:
#                 print('Error: No command found!')
#         else:
#             print('Error: No table found!')
#
#         # What I have now?
#         x = 'command: ' + command + '\tcolumns: ' + columns_ + '\ttable: ' + table + '\tconditions: ' + conditions_
#         print(x)
#
#         # Generate SQL query
#         if command == 'SELECT':
#             sql_ = command + " " + columns_ + " FROM " + table
#         elif command == 'UPDATE':
#             sql_ = command + " " + table + " SET " + updates_
#         elif command == 'DELETE':
#             sql_ = command + " FROM " + table
#         if conditions_:
#             sql_ += " " + conditions_
#         sql_ += ';'
#
#         return sql_
#
#
# def listToTuple(tuple_, result_):
#     j = list(tuple_)
#     j.append(result_[1])
#     j.append(result_[0])
#     return tuple(j)
