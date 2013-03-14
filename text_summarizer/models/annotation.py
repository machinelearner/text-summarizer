from text_summarizer.models import Article
from django.db import models
import math
from django.db.models import Max

class Annotation(models.Model):
    WORD_TYPE = (
            ('cue','cue words'),
            ('ner','named entity'),
            )
    word = models.CharField(max_length=500)
    term_frequency = models.FloatField()
    document_frequency = models.FloatField()
    word_type = models.CharField(max_length=3,
                                      choices=WORD_TYPE,
                                      default=WORD_TYPE[0][0])
    class Meta:
        app_label = 'text_summarizer'

    def tfidf(self):
        number_of_documents = Article.objects.count()
        tfidf = (self.term_frequency/self.max_tf()) * math.log(((number_of_documents + 1)/self.document_frequency),2)
        return round(tfidf,4)

    @classmethod
    def max_tf(self):
        return self.objects.all().aggregate(Max('term_frequency'))['term_frequency__max']
