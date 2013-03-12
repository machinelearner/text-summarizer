from django.db import models
from text_summarizer.models import Article
from collections import defaultdict,OrderedDict

class ArticleEditSummarySentence(models.Model):
    paragraph_number = models.IntegerField()
    content = models.TextField(max_length=25000)
    article = models.ForeignKey(Article)

    class Meta:
        app_label = 'text_summarizer'

