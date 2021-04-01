from sinling import SinhalaTokenizer, POSTagger
from service.stemming import Stemming


class Tokenization:

    def __init__(self):
        self.tokenizer = SinhalaTokenizer()
        self.tagger = POSTagger()
        self.stemming = Stemming()

    def posTagger(self, sentence):

        # tokenization
        tokens = [self.tokenizer.tokenize(f'{ss}.') for ss in self.tokenizer.split_sentences(sentence)]

        # Stemming
        stems = []
        for token in tokens[0]:
            stems.append(self.stemming.findRoot(token))

        # POS Tagging
        pos_tags = self.tagger.predict([stems])
        return pos_tags
