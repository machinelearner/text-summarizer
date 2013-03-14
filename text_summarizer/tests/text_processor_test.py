from django.test import TestCase
from text_summarizer.models import TextProcessor

class TextProcessorTest(TestCase):
    content = ''
    def setUp(self):
        self.text_processor = TextProcessor()
        self.content = """This is part of the test content.
        Sentence consists of nouns and other things, really? Los Angeles is the city of Angels."""

    def testShouldExtractWordsFromASentenceExcludingStopWords(self):
        #test to validate the regex
        identified_unique_tokens = self.text_processor.tokenize(self.content)
        self.assertEqual(len(identified_unique_tokens),10)
        actual_stopped_unique_tokens = ['test','part','content','sentence','consists','nouns','los','angeles','city','angels']
        self.assertEqual(sorted(identified_unique_tokens),sorted(actual_stopped_unique_tokens))

    def testShouldExtractSentencesGivenTextSplitByEolOrPeriods(self):
        #test to validate the regex
        identified_sentences = self.text_processor.sent_tokenize(self.content)
        self.assertEqual(len(identified_sentences),3)
        actual_sentences = ['This is part of the test content','Sentence consists of nouns and other things, really', 'Los Angeles is the city of Angels']
        self.assertEqual(sorted(identified_sentences),sorted(actual_sentences))

