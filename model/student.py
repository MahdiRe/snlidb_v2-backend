class Student:

    def __init__(self, name, age, marks):
        self.__name = name
        self.__age = age
        self.__marks = marks

    def to_string(self):
        return 'name : ' + self.__name + '\n' \
               'age : ' + self.__age + '\n' \
               'marks : ' + self.__marks
