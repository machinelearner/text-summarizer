from django.test import TestCase
from text_summarizer.models import UnigramDistribution,Article

class UnigramDistributionTest(TestCase):
    document = ''
    words = {}
    def setUp(self):
        document = Article(title="Title",content="Peter Piper picked a peck of pickled peppers.Did Peter Piper pick a peck of pickled peppers")
        words = {"peter": 2,
                "piper":2,
                "picked":1,
                "peck":2,
                "pickled":2,
                "peppers":2,
                "pick":1
                }

    def testShouldGetTermFrequencies():
        

