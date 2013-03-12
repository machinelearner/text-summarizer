from django.db import models

class Annotation(models.Model):
    WORD_TYPE = (
            ('cue','cue words'),
            ('ner','named entity'),
            )
    word = models.CharField(max_length=500)
    weight = models.FloatField()
    word_type = models.CharField(max_length=3,
                                      choices=WORD_TYPE,
                                      default=WORD_TYPE[0][0])
    class Meta:
        app_label = 'text_summarizer'
