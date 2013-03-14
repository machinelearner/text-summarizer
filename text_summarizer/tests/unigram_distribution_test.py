from django.test import TestCase
from text_summarizer.models import UnigramDistribution,Article,Annotation
from numpy import array

class UnigramDistributionTest(TestCase):
    documents = []
    term_frequencies = {}
    document_frequencies = {}
    def setUp(self):
        article1 = Article(title="Title",content="Peter Piper picked a peck of pickled peppers.Did Peter Piper pick a peck of pickled peppers")
        article2 = Article(title="Title",content="Peter Piper picked a peck of pickled peppers.")
        article1.save()
        article2.save()
        self.documents =[article1,article2]
        self.term_frequencies = {"peter": 3,
                "piper":3,
                "pickled":3,
                "picked":2,
                "pick":1,
                "peppers":3,
                "peck":3
                }
        self.document_frequencies = {"peter": 2,
                "piper":2,
                "pickled":2,
                "picked":2,
                "pick":1,
                "peppers":2,
                "peck":2
                }

    def testShouldGenerateTermFrequencies(self):
        tf = UnigramDistribution.generate_tf(self.documents)
        print(tf)
        expected_number_of_annotations = len(self.term_frequencies.keys())
        annotations_generated = len(tf.keys())
        self.assertTrue(self.term_frequencies == tf)
        self.assertEqual(expected_number_of_annotations,annotations_generated)

    def testShouldGenerateDocumentFrequencies(self):
        df = UnigramDistribution.generate_df(self.documents)
        print(df)
        expected_number_of_annotations = len(self.document_frequencies.keys())
        annotations_generated = len(df.keys())

        self.assertEqual(expected_number_of_annotations,annotations_generated)
        self.assertTrue(self.document_frequencies == df)

    def testShouldGenerateTermAndDocumentFrequenciesForAnnotations(self):
        UnigramDistribution.generate_tf_df(self.documents)
        number_of_annotations_generated = Annotation.objects.count()
        number_of_annotations_expected_by_tf = len(self.term_frequencies.keys())
        number_of_annotations_expected_by_df = len(self.document_frequencies.keys())
        created_annotations = Annotation.objects.all()

        self.assertEqual(number_of_annotations_generated,number_of_annotations_expected_by_tf)
        self.assertEqual(number_of_annotations_generated,number_of_annotations_expected_by_df)
        for annotation in created_annotations:
            self.assertTrue(annotation.word in self.term_frequencies)
            self.assertTrue(annotation.word in self.document_frequencies)
            self.assertEqual(annotation.term_frequency,self.term_frequencies[annotation.word])
            self.assertEqual(annotation.document_frequency,self.document_frequencies[annotation.word])

    def testShouldGenerateVectorGiven_all_TokensAndText(self):
        UnigramDistribution.generate_tf_df(self.documents)
        text = "Peter pickled pick piper"
        corpus_tokens = self.term_frequencies.keys()
        vector = UnigramDistribution.generate_vector(text,corpus_tokens)
        expected_vector = array([0,0.585,0.585,0,0.5283,0,0.585])
        self.assertEqual(vector.all(),expected_vector.all())

