from sinling import SinhalaTokenizer, POSTagger
from service.stemming import Stemming


class Tokenization:

    def __init__(self):
        self.__tokenizer = SinhalaTokenizer()
        self.__tagger = POSTagger()
        self.__stemming = Stemming()

    def pos_tagger(self, sentence):

        # tokenization
        tokens = [self.__tokenizer.tokenize(f'{ss}.') for ss in self.__tokenizer.split_sentences(sentence)]

        # Stemming
        stems = []
        for token in tokens[0]:
            stems.append(self.__stemming.find_root(token))

        # POS Tagging
        pos_tags = self.__tagger.predict([stems])
        return pos_tags
