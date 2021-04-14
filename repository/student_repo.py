from repository.db import Db


class StudentRepo(Db):

    def __init__(self):
        super().__init__()

    def execute_query(self, query):
        try:
            # Create cursor
            cursor = self._conn.cursor()
            # cursor.execute("insert into patient(name,age) values (%s,%s)", (name, age))
            cursor.execute(query)
            self._conn.commit()
            # records = cursor.fetchall()
            result = [dict((cursor.description[i][0], value)
                            for i, value in enumerate(row)) for row in cursor.fetchall()]
            cursor.close()
        except Exception as e:
            print('Exception : ' + str(e))
            result = 'Exception found!'
        return result

    def insert_student(self, name, age, marks):
        try:
            # Create cursor
            cursor = self._conn.cursor()
            cursor.execute("INSERT INTO student(name, age, marks) VALUES (%s, %s, %s)", (name, age, marks))
            # cursor.execute(query)
            self._conn.commit()
            # records = cursor.fetchall()
            result = [dict((cursor.description[i][0], value)
                           for i, value in enumerate(row)) for row in cursor.fetchall()]
            cursor.close()
        except Exception as e:
            print('Exception : ' + str(e))
            result = 'Exception found!'
        return result
