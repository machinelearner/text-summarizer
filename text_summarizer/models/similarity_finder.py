from text_summarizer.models import *
from collections import defaultdict,OrderedDict
import math
import nltk
from nltk import cluster
from nltk.cluster import euclidean_distance
from numpy import array

class SimilarityFinder():
    class Meta:
        app_label = 'text_summarizer'

    @staticmethod
    def cluster_paragraphs(original_sentences_list,sample_sentences_list):
        tokens = []
        for sent in original_sentences_list:
            tokens += TextProcessor().tokenize(sent)
        for sent in sample_sentences_list:
            tokens += TextProcessor().tokenize(sent)
        tokens = OrderedDict.fromkeys(tokens).keys()
        #print("################################")
        #print(tokens)
        #print("################################")
        initial_vectors = map(lambda sentence: UnigramDistribution.generate_vector(sentence,tokens),original_sentences_list)
        sample_distribution = map(lambda sentence: UnigramDistribution.generate_vector(sentence,tokens),sample_sentences_list)
        all_sentences = original_sentences_list + sample_sentences_list
        clusterer = cluster.em.EMClusterer(initial_vectors)
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
    def isSimilar(comparision_sentences,new_sentence):
        tokens = []
        for sent in original_sentences_list:
            tokens += TextProcessor().tokenize(sent)
        for sent in sample_sentences_list:
            tokens += TextProcessor().tokenize(sent)
        tokens = OrderedDict.fromkeys(tokens).keys()
        #print("################################")
        #print(tokens)
        #print("################################")
        initial_vectors = map(lambda sentence: UnigramDistribution.generate_vector(sentence,tokens),original_sentences_list)
        sample_distribution = map(lambda sentence: UnigramDistribution.generate_vector(sentence,tokens),sample_sentences_list)
        all_sentences = original_sentences_list + sample_sentences_list
        clusterer = cluster.em.EMClusterer(initial_vectors)
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

