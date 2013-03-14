from django.test import TestCase
from text_summarizer.models import Article

class ArticleTest(TestCase):
    title = []
    content = []
    def setUp(self):
        title1 = 'This is a test article'
        content1 = 'This is part of the test content. Sentence consists of nouns and other things. Los Angeles is the city of Angels.'
        self.title.append(title1)
        self.content.append(content1)
        self.dummy_article = Article(title=title1,content=content1)
        self.dummy_article.save()

    #Integration kind of test
    def testShouldCreateArticleWithoutAssociatedAnnotation(self):
        #1 object already created during setUp method
        title2 = 'This is another article'
        content2 = 'The content does not have any structure of any sort and is designed just to HOST few nouns so that they can be used in this particular test'
        dummy_article2 = Article(title=title2,content=content2)
        dummy_article2.save()
        self.content.append(content2)
        self.title.append(title2)
        self.assertEqual(Article.objects.count(),2)
        articles = Article.objects.all()
        for i,art in enumerate(articles):
            self.assertEqual(self.title[i],art.title)
            self.assertEqual(self.content[i],art.content)
