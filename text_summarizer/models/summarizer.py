from text_summarizer.models import TextProcessor,ArticleEditSummarySentence,SimilarityFinder,Annotation,CosineSimilarity,UnigramDistribution
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
        sentence_dict = self.sentence_weights(sentences)
        print(sentence_dict)
        sentence_number_sorted_by_weights = sorted(sentence_dict,key=sentence_dict.get,reverse=True)
        summary_sentences = []
        number_of_sentences_in_summary = int(math.ceil(self.COMPRESSION * len(sentences)))
        for sentence_number in sorted(sentence_number_sorted_by_weights[:number_of_sentences_in_summary]):
            summary_sentences.append(sentences[sentence_number])
        return summary_sentences

    #def summarize_using_cosine_similarity_constant(self,content):
        #sentences =self.text_processor.nltk_sentences(content)
        #tokens_in_content = self.text_processor.tokenize(content)
        #sentence_dict = defaultdict(int)
        #for sentence_number,sentence in enumerate(sentences):
            #if (self.text_processor.is_blank(sentence)):
                #continue
            #sentence_vector = UnigramDistribution.generate_vector(sentence,tokens_in_content)
            #sentence_dict[sentence_number] = CosineSimilarity.calculate(sentence_vector,document_vector)

        #sentence_number_sorted_by_weights = sorted(sentence_dict,key=sentence_dict.get,reverse=True)
        #summary_sentences = []
        #number_of_sentences_in_summary = int(math.ceil(self.COMPRESSION * len(sentences)))
        #for sentence_number in sorted(sentence_number_sorted_by_weights[:number_of_sentences_in_summary]):
            #summary_sentences.append(sentences[sentence_number])
        #return summary_sentences

    #def sentence_weight(self,sentence,sentence_number,number_of_sentences):
        #sentence_location_weight = self.get_sentence_location_weight(sentence_number,number_of_sentences)
        #word_weight_aggregation = self.get_word_weight_aggregation(sentence)
        #n_e_r_weight = self.get_n_e_r_weight(sentence)
        #weight_of_sentence = self.ALPHA * sentence_location_weight + self.BETA * word_weight_aggregation + self.GAMMA * n_e_r_weight
        #return weight_of_sentence

    def sentence_weights(self,sentences):
        sentence_dict = defaultdict(float)
        max_tfidf = UnigramDistribution.max_tfidf()
        location_weights = []
        for sent_number,sent in enumerate(sentences):
            location_weights.append(self.get_sentence_location_weight(sent_number,len(sentences)))
        tfidf_weigths = map(lambda sent: self.get_word_weight_aggregation(sent),sentences)
        normalized_tfidf_weights = map(lambda w: w/max_tfidf,tfidf_weigths)
        n_e_r_weights = map(lambda sent: self.get_n_e_r_weight(sent),sentences)
        print(n_e_r_weights)
        normalized_n_e_r = self.normList(n_e_r_weights)
        for sentence_number,sentence in enumerate(sentences):
            if (self.text_processor.is_blank(sentence)):
                continue
            weight_of_sentence = self.ALPHA * location_weights[sentence_number] + self.BETA * normalized_tfidf_weights[sentence_number] + self.GAMMA * normalized_n_e_r[sentence_number]
            sentence_dict[sentence_number] = round(weight_of_sentence/(self.ALPHA + self.BETA + self.GAMMA),4)
        return sentence_dict


    def summarize_using_cosine_similarity(self,content):
        sentences =self.text_processor.nltk_sentences(content)
        tokens_in_content = self.text_processor.tokenize(content)
        document_vector = UnigramDistribution.generate_vector(content,tokens_in_content)
        number_of_sentences_in_summary = int(math.ceil(self.COMPRESSION * len(sentences)))
        summary_sentences = []
        print("Sentences in summary(order of relevance)")
        for i in range(0,number_of_sentences_in_summary):
            sentence_dict = defaultdict(int)
            for sentence_number,sentence in enumerate(sentences):
                if (self.text_processor.is_blank(sentence) or sentence_number in summary_sentences):
                    continue
                sentence_vector = UnigramDistribution.generate_vector(sentence,tokens_in_content)
                sentence_dict[sentence_number] = CosineSimilarity.calculate(sentence_vector,document_vector)
            highest_similarity_sentence_number = sorted(sentence_dict,key=sentence_dict.get,reverse=True)[0]
            print(highest_similarity_sentence_number)
            summary_sentences.append(highest_similarity_sentence_number)
            tokens_in_sentence = self.text_processor.tokenize(sentences[highest_similarity_sentence_number])
            tokens_in_content = filter(lambda token: token not in tokens_in_sentence,tokens_in_content)
            document_vector = UnigramDistribution.generate_vector(content,tokens_in_content)
        summary = []
        for sentence_number in sorted(summary_sentences):
            summary.append(sentences[sentence_number])
        return summary

    def summarize_using_cos_and_weights(self,content):
        sentences =self.text_processor.nltk_sentences(content)
        sentence_weights = self.sentence_weights(sentences)
        tokens_in_content = self.text_processor.tokenize(content)
        document_vector = UnigramDistribution.generate_vector(content,tokens_in_content)
        number_of_sentences_in_summary = int(math.ceil(self.COMPRESSION * len(sentences)))
        summary_sentences = []
        print("Sentences in summary(order of relevance)")
        for i in range(0,number_of_sentences_in_summary):
            sentence_dict = defaultdict(int)
            for sentence_number,sentence in enumerate(sentences):
                if (self.text_processor.is_blank(sentence) or sentence_number in summary_sentences):
                    continue
                sentence_vector = UnigramDistribution.generate_vector(sentence,tokens_in_content)
                sentence_dict[sentence_number] = CosineSimilarity.calculate(sentence_vector,document_vector) + sentence_weights[sentence_number]
            highest_similarity_sentence_number = sorted(sentence_dict,key=sentence_dict.get,reverse=True)[0]
            print(highest_similarity_sentence_number)
            summary_sentences.append(highest_similarity_sentence_number)
            tokens_in_sentence = self.text_processor.tokenize(sentences[highest_similarity_sentence_number])
            tokens_in_content = filter(lambda token: token not in tokens_in_sentence,tokens_in_content)
            document_vector = UnigramDistribution.generate_vector(content,tokens_in_content)
        summary = []
        for sentence_number in sorted(summary_sentences):
            summary.append(sentences[sentence_number])
        return summary

    def summarize_edits_for_article(self,article):
        original_paragraphs = article.paragraphs()
        edited_paragraphs = article.articleedit_set.all()
        edited_paragraph_numbers = OrderedDict.fromkeys(map(lambda paragraph: paragraph.paragraph_number,edited_paragraphs)).keys()
        ArticleEditSummarySentence.objects.filter(article=article).delete()
        edits_summary = defaultdict(list)

        for paragraph_number in edited_paragraph_numbers:
            original_paragraph = original_paragraphs[paragraph_number]
            #original_sentences = self.text_processor.sent_tokenize(original_paragraph)
            original_sentences = self.text_processor.nltk_sentences(original_paragraph)
            edits_for_paragraph = map(lambda paragraph: paragraph.content,edited_paragraphs.filter(paragraph_number=paragraph_number))
            sentences_in_edits = []
            for para in edits_for_paragraph:
                #sentences_in_edits += self.text_processor.sent_tokenize(para)
                sentences_in_edits += self.text_processor.nltk_sentences(para)
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
        #number_of_summary_sentences = 2#number_of_clusters
        """revisit number of sentence selection"""
        weighted_sentences = defaultdict(float)
        for index,sentence in enumerate(sentences):
            if self.text_processor.is_blank(sentence):
                continue
            word_weight_aggregation = self.get_word_weight_aggregation(sentence)
            n_e_r_weight = self.get_n_e_r_weight(sentence)
            weight = self.BETA * word_weight_aggregation + self.GAMMA * n_e_r_weight
            weight = round(weight/2.0,4)
            weighted_sentences[index] = weight
        summary_sentences = []
        sentence_number_sorted_by_weights = sorted(weighted_sentences,key=weighted_sentences.get,reverse=True)
        for sentence_number in sentence_number_sorted_by_weights:
            if(SimilarityFinder.isNotSimilar(summary_sentences,sentences[sentence_number])):
                summary_sentences.append(sentences[sentence_number])
        return summary_sentences

    def get_sentence_location_weight(self,sentence_number,number_of_sentences):
        location_weight = 1 - sentence_number/float(number_of_sentences)
        return round(location_weight,4)

    def get_word_weight_aggregation(self,sentence):
        words = self.text_processor.tokenize(sentence)
        annotations = Annotation.objects.filter(word__in=words)
        sigma_weight = 0
        max_tfidf_in_sentence = -1
        for annotation in annotations:
            tfidf = annotation.tfidf()
            max_tfidf_in_sentence = tfidf if max_tfidf_in_sentence < tfidf else max_tfidf_in_sentence
            sigma_weight += tfidf
        normalized_sigma_weight = sigma_weight/(len(words)*max_tfidf_in_sentence) if len(words) != 0 else 0
        return normalized_sigma_weight

    def get_n_e_r_weight(self,sentence):
        NER_tree = self.text_processor.extract_ner_tree(sentence)
        if not(NER_tree):
            return 0
        number_of_NERs = reduce(lambda value1,value2: value1+value2,map(lambda node: 1 if isinstance(node,nltk.tree.Tree) else 0,NER_tree))
        return number_of_NERs

    @staticmethod
    def normList(L, normalizeTo=1):
        '''normalize values of a list to make its max = normalizeTo'''

        vMax = max(L)
        return [ x/(vMax*1.0)*normalizeTo for x in L]
