from text_summarizer.models import *
from collections import defaultdict,OrderedDict
import math
import nltk


class Summarizer():
    ALPHA = 1
    BETA = 1
    GAMMA = 2
    COMPRESSION = 0.30
    class Meta:
        app_label = 'text_summarizer'

    def get_sentence_location_weight(self,sentence_number,number_of_sentences):
        location_weight = 1 - sentence_number/float(number_of_sentences)
        return round(location_weight,4)

    def get_word_weight_aggregation(self,sentence):
        words = TextProcessor().tokenize(sentence)
        annotations = Annotation.objects.filter(word__in=words)
        sigma_weight = 0
        for annotation in annotations:
            sigma_weight += annotation.weight
        normalized_sigma_weight = sigma_weight/len(words) if len(words) != 0 else 0
        return normalized_sigma_weight

    def get_n_e_r_weight(self,sentence):
        tokens = TextProcessor().no_stop_tokens(sentence)
        pos_tagged_sentence = nltk.pos_tag(tokens)
        NER_tree = nltk.ne_chunk(pos_tagged_sentence,binary=True)
        if not(NER_tree):
            return 0
        number_of_NERs = reduce(lambda value1,value2: value1+value2,map(lambda node: 1 if isinstance(node,nltk.tree.Tree) else 0,NER_tree))
        return number_of_NERs

    def summarize_sentences(self,sentences,number_of_clusters):
        number_of_summary_sentences = 2#number_of_clusters
        weighted_sentences = defaultdict(float)
        for index,sentence in enumerate(sentences):
            word_weight_aggregation = self.get_word_weight_aggregation(sentence)
            n_e_r_weight = self.get_n_e_r_weight(sentence)
            weight = self.BETA * word_weight_aggregation + self.GAMMA * n_e_r_weight
            weight = round(weight/2.0,4)
            weighted_sentences[index] = weight
        summary_sentences = []
        sentence_number_sorted_by_weights = sorted(weighted_sentences,key=weighted_sentences.get,reverse=True)
        for sentence_number in sentence_number_sorted_by_weights[:number_of_summary_sentences]:
            if(SimilarityFinder.isSimilar(summary_sentences,sentences[sentence_number])):
                summary_sentences.append(sentences[sentence_number])
        return summary_sentences


    def summarize_article(self,article):
        content = article.content
        sentences =TextProcessor().sent_tokenize(content)
        sentence_dict = defaultdict(int)
        for sentence_number,sentence in enumerate(sentences):
            if (TextProcessor().is_blank(sentence)):
                continue
            sentence_location_weight = self.get_sentence_location_weight(sentence_number,len(sentences))
            word_weight_aggregation = self.get_word_weight_aggregation(sentence)
            n_e_r_weight = self.get_n_e_r_weight(sentence)
            weight_of_sentence = self.ALPHA * sentence_location_weight + self.BETA * word_weight_aggregation + self.GAMMA * n_e_r_weight
            sentence_dict[sentence_number] = round(weight_of_sentence/3.0,4)
        sentence_number_sorted_by_weights = sorted(sentence_dict,key=sentence_dict.get,reverse=True)
        summary_sentences = []
        number_of_sentences_in_summary = int(math.ceil(self.COMPRESSION * len(sentences)))
        for sentence_number in sorted(sentence_number_sorted_by_weights[:number_of_sentences_in_summary]):
            summary_sentences.append(sentences[sentence_number])
        return summary_sentences

    def summarize_edits_for_article(self,article):
        original_paragraphs = article.paragraphs()
        edited_paragraphs = article.articleedit_set.all()
        edited_paragraph_numbers = OrderedDict.fromkeys(map(lambda paragraph: paragraph.paragraph_number,edited_paragraphs)).keys()
        #print("######################")
        #print(edited_paragraph_numbers)
        edits_summary = defaultdict(list)
        for paragraph_number in edited_paragraph_numbers:
            original_paragraph = original_paragraphs[paragraph_number]
            original_sentences = TextProcessor().sent_tokenize(original_paragraph)
            edits_for_paragraph = map(lambda paragraph: paragraph.content,edited_paragraphs.filter(paragraph_number=paragraph_number))
            sentences_in_edits = []
            for para in edits_for_paragraph:
                sentences_in_edits += TextProcessor().sent_tokenize(para)
            similar_sentences = SimilarityFinder.cluster_paragraphs(original_sentences,sentences_in_edits)
            summary_sentences = []
            for group,sentences in similar_sentences.items():
                summary_sentences += self.summarize_sentences(sentences,len(similar_sentences.keys()))
            edits_summary[paragraph_number] += summary_sentences
        return edits_summary
