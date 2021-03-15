from flask_googletrans import translator

class Translation:

    def translate(self, sentence, app):
        ts = translator(app)
        t = ts.translate(sentence, 'si', ['en'])
        return t