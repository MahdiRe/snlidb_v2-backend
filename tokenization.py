from sinling import SinhalaTokenizer, POSTagger

class Tokenization:

    def __init__(self):
        self.tokenizer = SinhalaTokenizer()

    def posTagger(self, sentence):
        tagger = POSTagger()

        tokens = [self.tokenizer.tokenize(f'{ss}.') for ss in self.tokenizer.split_sentences(sentence)]
        pos_tags = tagger.predict(tokens)

        print(pos_tags)

        return pos_tags