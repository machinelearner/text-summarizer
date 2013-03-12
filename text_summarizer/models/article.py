from django.db import models
from text_summarizer.models import *

POS_TAGS = ["NN","NNS","NNP","NNPS"]

class Article(models.Model):
    title = models.CharField(max_length=500)
    content = models.TextField(max_length=25000)

    class Meta:
        app_label = 'text_summarizer'


    def tokenize(self):
        tokens = TextProcessor().tokenize(self.content)
        return tokens

    def paragraphs(self):
        paragraphs = self.content.split('\n')
        return paragraphs


    #def extract_key_words(self):
         #Difinition of Key Word is based on the TF-IDF value of the annotations in the document.
        #extract_nouns()
        #annotations = map(lambda x: str(x.word),self.annotation_set.all())

