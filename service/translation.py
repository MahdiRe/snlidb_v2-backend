from flask_googletrans import translator


class Translation:

    def __init__(self, app):
        self.ts = translator(app)

    def translate(self, sentence, app):
        translated_word = self.ts.translate(sentence, 'si', ['en'])
        return translated_word
