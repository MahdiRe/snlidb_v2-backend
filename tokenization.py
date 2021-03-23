from sinling import SinhalaTokenizer, POSTagger
from stemming import Stemming
from condition_extractor import ConditionExtractor


class Tokenization:

    def __init__(self):
        self.tokenizer = SinhalaTokenizer()
        self.tagger = POSTagger()
        self.stemming = Stemming()
        self.conx = ConditionExtractor()

    def posTagger(self, sentence):

        # tokenization
        tokens = [self.tokenizer.tokenize(f'{ss}.') for ss in self.tokenizer.split_sentences(sentence)]
        # print(tokens)

        # Remove ක්, ක, ත්, වූ, වු in numbers only
        # tokens = [self.conx.num_issue(tokens[0])]
        # print(tokens)

        # Stemming
        stems = []
        for token in tokens[0]:
            stems.append(self.stemming.findRoot(token))
        # print('stems: ' + str(stems))

        # POS Tagging
        pos_tags = self.tagger.predict([stems])
        return pos_tags
