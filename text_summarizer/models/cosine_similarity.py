from math import sqrt
class CosineSimilarity:

    class Meta:
        app_label = 'text_summarizer'

    @staticmethod
    def calculate(vectorA,vectorB):
        dot_product = reduce(lambda x,y: x+y,map(lambda Ai,Aj: Ai*Aj,vectorA,vectorB))
        vectorA_norm = sqrt(reduce(lambda x,y: x+y,map(lambda Ai: Ai*Ai,vectorA)))
        vectorB_norm = sqrt(reduce(lambda x,y: x+y,map(lambda Bi: Bi*Bi,vectorB)))
        cosine_similarity_score = dot_product/(vectorA_norm*vectorB_norm)
        return cosine_similarity_score

