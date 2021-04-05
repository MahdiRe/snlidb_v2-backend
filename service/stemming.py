class Stemming:

    def __init__(self):
        self.__create_stem_dictionary()
        self.__stemmer_dict = {}

    def __create_stem_dictionary(self):
        file = open('sinhala_stemmer.txt', encoding='UTF-8')
        lines = file.readlines()

        for line in lines:
            line = line.split('\t')
            self.__stemmer_dict[line[0].strip()] = line[1].strip('\n')

    def find_root(self, word):
        stem = self.__stemmer_dict.get(word, word)
        return stem
