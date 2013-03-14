from text_summarizer.models import TextProcessor,ArticleEditSummarySentence,SimilarityFinder,Annotation
from collections import defaultdict,OrderedDict
import math
import nltk


class Summarizer():
    text_processor = TextProcessor()
    ALPHA = 1
    BETA = 1
    GAMMA = 2
    COMPRESSION = 0.30
    NUMBER_OF_WEIGHTING_MEASURES = 3.0
    class Meta:
        app_label = 'text_summarizer'

    def summarize(self,content):
        sentences =self.text_processor.nltk_sentences(content)
        sentence_dict = defaultdict(int)
        for sentence_number,sentence in enumerate(sentences):
            if (self.text_processor.is_blank(sentence)):
                continue
            weight_of_sentence = self.sentence_weight(sentence,sentence_number,len(sentences))
            sentence_dict[sentence_number] = round(weight_of_sentence/self.NUMBER_OF_WEIGHTING_MEASURES,4)

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
        ArticleEditSummarySentence.objects.filter(article=article).delete()
        edits_summary = defaultdict(list)

        for paragraph_number in edited_paragraph_numbers:
            original_paragraph = original_paragraphs[paragraph_number]
            original_sentences = self.text_processor.sent_tokenize(original_paragraph)
            edits_for_paragraph = map(lambda paragraph: paragraph.content,edited_paragraphs.filter(paragraph_number=paragraph_number))
            sentences_in_edits = []
            for para in edits_for_paragraph:
                sentences_in_edits += self.text_processor.sent_tokenize(para)
            similar_sentences = SimilarityFinder.cluster_paragraphs(original_sentences,sentences_in_edits)
            summary_sentences = []
            for group,sentences in similar_sentences.items():
                summary_sentences += self.summarize_sentences(sentences,len(similar_sentences.keys()))
            edits_summary[paragraph_number] += summary_sentences
            for sentence in summary_sentences:
                summary_sentence = ArticleEditSummarySentence(paragraph_number=paragraph_number,content=sentence,article=article)
                summary_sentence.save()
        return edits_summary

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
            if(SimilarityFinder.isNotSimilar(summary_sentences,sentences[sentence_number])):
                summary_sentences.append(sentences[sentence_number])
        return summary_sentences

    def sentence_weight(self,sentence,sentence_number,number_of_sentences):
        sentence_location_weight = self.get_sentence_location_weight(sentence_number,number_of_sentences)
        word_weight_aggregation = self.get_word_weight_aggregation(sentence)
        n_e_r_weight = self.get_n_e_r_weight(sentence)
        weight_of_sentence = self.ALPHA * sentence_location_weight + self.BETA * word_weight_aggregation + self.GAMMA * n_e_r_weight
        return weight_of_sentence

    def get_sentence_location_weight(self,sentence_number,number_of_sentences):
        location_weight = 1 - sentence_number/float(number_of_sentences)
        return round(location_weight,4)

    def get_word_weight_aggregation(self,sentence):
        words = self.text_processor.tokenize(sentence)
        annotations = Annotation.objects.filter(word__in=words)
        sigma_weight = 0
        for annotation in annotations:
            sigma_weight += annotation.tfidf()
        normalized_sigma_weight = sigma_weight/len(words) if len(words) != 0 else 0
        return normalized_sigma_weight

    def get_n_e_r_weight(self,sentence):
        NER_tree = self.text_processor.extract_ner_tree(sentence)
        if not(NER_tree):
            return 0
        number_of_NERs = reduce(lambda value1,value2: value1+value2,map(lambda node: 1 if isinstance(node,nltk.tree.Tree) else 0,NER_tree))
        return number_of_NERs
