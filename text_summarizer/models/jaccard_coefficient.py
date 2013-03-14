from text_summarizer.models import TextProcessor

class JaccardCoefficient():

    class Meta:
        app_label = 'text_summarizer'

    @staticmethod
    def calculate(sentence1,sentence2):
        tokens1 = TextProcessor().tokenize(sentence1)
        tokens2 = TextProcessor().tokenize(sentence2)
        cardinality_of_intersection = len(set(tokens1) & set(tokens2))
        cardinality_of_union = len(set(tokens1) | set(tokens2))
        jIndex = round(cardinality_of_intersection/float(cardinality_of_union),4)
        return jIndex

