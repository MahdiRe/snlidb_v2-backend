class Stemming:

    def __init__(self):
        self.stemmer_dict = {}
        self.create_stem_dictionary()

    def create_stem_dictionary(self):
        file = open('sinhala_stemmer.txt', encoding='UTF-8')
        lines = file.readlines()

        for line in lines:
            line = line.split('\t')
            self.stemmer_dict[line[0].strip()] = line[1].strip('\n')

    def find_root(self, word):
        stem = self.stemmer_dict.get(word, word)
        return stem
