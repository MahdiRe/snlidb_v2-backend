class Stemming:

    stemmer_dict = {}

    def __init__(self):
        self.createStemDictionary()

    def createStemDictionary(self):
        file = open('sinhala_stemmer.txt', encoding='UTF-8')
        lines = file.readlines()

        for line in lines:
            line = line.split('\t')
            self.stemmer_dict[line[0].strip()] = line[1].strip('\n')

    def findRoot(self, word):
        stem = self.stemmer_dict.get(word)
        return stem