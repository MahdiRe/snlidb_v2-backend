from repository.db import Db
import sys


class StudentRepo(Db):

    def __init__(self):
        super().__init__()

    def executeQuery(self, query):
        try:
            # Create cursor
            cursor = self.conn.cursor()
            # cursor.execute("insert into patient(name,age) values (%s,%s)", (name, age))
            cursor.execute(query)
            self.conn.commit()
            records = cursor.fetchall()
            cursor.close()
        except:
            e = sys.exc_info()[0]
            print('Exception : ' + str(e))
            records = 'Exception found!'
        return records
