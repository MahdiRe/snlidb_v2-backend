from repository.db import Db


class UserRepo(Db):

    def __init__(self):
        super().__init__()

    def insert_user(self, u_name, pwd, role):
        try:
            cursor = self._conn.cursor()
            cursor.execute("INSERT INTO users(user_name, password, role) values (%s, %s, %s)", (u_name, pwd, role))
            self._conn.commit()
            result = [dict((cursor.description[i][0], value)
                           for i, value in enumerate(row)) for row in cursor.fetchall()]
            cursor.close()
            if (type(result) is list) and (len(result) == 0):
                result = "Registered successfully"
        except Exception as e:
            print('Exception : ' + str(e))
            if e.args[0] == 1062:
                result = 'Username already taken!'
            else:
                result = self.handle_exceptions(e.args[0])
        return result

    def login_user(self, u_name, pwd):
        try:
            cursor = self._conn.cursor()
            cursor.execute("SELECT * FROM users WHERE user_name = %s and password = %s;", (u_name, pwd))
            self._conn.commit()
            result = [dict((cursor.description[i][0], value)
                           for i, value in enumerate(row)) for row in cursor.fetchall()]
            cursor.close()
        except Exception as e:
            print('Exception : ' + str(e))
            result = self.handle_exceptions(e.args[0])
        return result
