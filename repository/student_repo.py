from repository.db import Db


class StudentRepo(Db):

    def __init__(self):
        super().__init__()

    def insert_student(self, name, age, marks):
        try:
            cursor = self._conn.cursor()
            cursor.execute("INSERT INTO student(name, age, marks) VALUES (%s, %s, %s)", (name, age, marks))
            self._conn.commit()
            result = [dict((cursor.description[i][0], value)
                           for i, value in enumerate(row)) for row in cursor.fetchall()]
            cursor.close()
            if (type(result) is list) and (len(result) == 0):
                result = "Student added successfully"
        except Exception as e:
            print('Exception : ' + str(e))
            result = 'Exception found!'
        return result

    def execute_student_query(self, query):
        try:
            cursor = self._conn.cursor()
            cursor.execute(query)
            self._conn.commit()
            result = [dict((cursor.description[i][0], value)
                           for i, value in enumerate(row)) for row in cursor.fetchall()]
            cursor.close()
            if (type(result) is list) and (len(result) == 0):
                result = "SQL executed successfully"
        except Exception as e:
            print('Exception : ' + str(e))
            result = 'Exception found!'
        return result
