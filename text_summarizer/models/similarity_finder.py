from text_summarizer.models import TextProcessor,JaccardCoefficient,UnigramDistribution,Annotation
from collections import defaultdict,OrderedDict
from nltk import cluster

class SimilarityFinder():
    JACCARD_INDEX_SIMILARITY_THRESHOLD  = 0.5
    class Meta:
        app_label = 'text_summarizer'

    @staticmethod
    def cluster_paragraphs(original_sentences_list,sample_sentences_list):
        all_tokens = []
        for sent in original_sentences_list:
            all_tokens += TextProcessor().tokenize(sent)
        for sent in sample_sentences_list:
            all_tokens += TextProcessor().tokenize(sent)
        all_tokens = OrderedDict.fromkeys(all_tokens).keys()
        tokens = Annotation.get_top_10_tfidf_tokens_from_list(all_tokens)
        initial_vectors = map(lambda sentence: UnigramDistribution.generate_vector(sentence,tokens),original_sentences_list)
        sample_distribution = map(lambda sentence: UnigramDistribution.generate_vector(sentence,tokens),sample_sentences_list)
        all_sentences = original_sentences_list + sample_sentences_list
        clusterer = cluster.em.EMClusterer(initial_vectors,normalise=True)
        clusterer.cluster_vectorspace(sample_distribution)
        classification_distribution = initial_vectors + sample_distribution
        classified_vectors = map(lambda vector:clusterer.classify_vectorspace(vector),classification_distribution)
        cluster_sentences = defaultdict(list)
        for sentence_number, cluster_name in enumerate(classified_vectors):
            cluster_sentences[cluster_name].append(all_sentences[sentence_number])
        print("################################ Cluster sentences")
        print(cluster_sentences)
        print("################################")
        return cluster_sentences

    @staticmethod
    def isNotSimilar(comparision_sentences,new_sentence):
        for sentence in comparision_sentences:
            jaccard_index = JaccardCoefficient.calculate(sentence,new_sentence)
            if jaccard_index > SimilarityFinder.JACCARD_INDEX_SIMILARITY_THRESHOLD:
                return False
        return True
