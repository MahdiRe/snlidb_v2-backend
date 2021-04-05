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
            records = cursor.fetchall()
            cursor.close()
        except Exception as e:
            print('Exception : ' + str(e))
            records = 'Exception found!'
        return records
