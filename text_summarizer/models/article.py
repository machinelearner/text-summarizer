from django.db import models
from text_summarizer.models import TextProcessor

POS_TAGS = ["NN","NNS","NNP","NNPS"]

class Article(models.Model):
    title = models.CharField(max_length=500)
    content = models.TextField(max_length=25000)
    text_processor = TextProcessor()

    class Meta:
        app_label = 'text_summarizer'

    def tokenize(self):
        tokens = self.text_processor.tokenize(self.content)
        return tokens

    def paragraphs(self):
        paragraphs = self.content.split('\n')
        return paragraphs

    def paragraphs_with_edit_summary(self):
        paragraphs = self.paragraphs()
        paragraphs_with_edit_summary = [0] * len(paragraphs)
        for para_number, paragraph in enumerate(paragraphs):
            edit_sentences = map(lambda edit_sentence: edit_sentence.content,self.articleeditsummarysentence_set.all().filter(paragraph_number=para_number))
            paragraphs_with_edit_summary[para_number] = [paragraph,edit_sentences]
        return paragraphs_with_edit_summary

    def __unicode__(self):
        return unicode(self.pk)

