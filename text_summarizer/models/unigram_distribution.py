from text_summarizer.models import *
from collections import defaultdict,OrderedDict
import math
from numpy import array

class UnigramDistribution():

    class Meta:
        app_label = 'text_summarizer'

    @staticmethod
    def increment_distribution(distribution,key):
        distribution[key] += 1

    @staticmethod
    def get_weight(weighted_annotation,vector_candidates):
        if(weighted_annotation.word in vector_candidates):
            return weighted_annotation.weight
        else:
            return 0


    @staticmethod
    def generate_tfidf():
        Annotation.objects.all().delete()
        articles = Article.objects.all()
        tf = defaultdict(int)
        df = defaultdict(int)
        tfidf = defaultdict(int)
        number_of_documents = len(articles)
        for article in articles:
            tokens = article.tokenize()
            [UnigramDistribution.increment_distribution(tf,token) for token in tokens]
            [UnigramDistribution.increment_distribution(df,token) for token in OrderedDict.fromkeys(tokens).keys()]

        max_tfidf = -1
        for token in tf.keys():
            tfidf[token] = tf[token] * round(math.log((number_of_documents+1)/float(df[token]),2),4)
            print("%s, tfidf = %f, tf = %f, df = %f" %(token.encode('utf-8'),tfidf[token],tf[token],df[token]))
            max_tfidf = tfidf[token] if max_tfidf < tfidf[token] else max_tfidf

        for token in tfidf.keys():
            normalized_tfidf = tfidf[token]/max_tfidf
            annotation = Annotation(word=token,weight=normalized_tfidf,word_type=Annotation.WORD_TYPE[0][0])
            annotation.save()

    @staticmethod
    def generate_vector(text,corpus_tokens):
        #Assumption: the unigram distribution of annotations is modelled into VS. Space is defined by dimension number which is in the DB record
        annotations = Annotation.objects.filter(word__in=corpus_tokens)
        tokens = TextProcessor().tokenize(text)
        vector_array = map(lambda annotation: UnigramDistribution.get_weight(annotation,tokens),annotations)
        print(vector_array)
        return array(vector_array)
