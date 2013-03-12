from django.contrib import admin
from text_summarizer.models import *

class ArticleAdmin(admin.ModelAdmin):
    fields = ['title','content']
    list_display = ('title','pk')
    list_filter = ('title',)
    search_fields = ['title','content']

class AnnotationAdmin(admin.ModelAdmin):
    list_display = ('word','weight')
    list_filter = ('word','weight')
    search_fields = ['word']

class ArticleEditAdmin(admin.ModelAdmin):
    list_display = ('content','paragraph_number','article',)
    search_fields = ['content','article']

class ArticleEditSummarySentenceAdmin(admin.ModelAdmin):
    list_display = ('content','paragraph_number','article',)
    search_fields = ['content']



admin.site.register(Article,ArticleAdmin)
admin.site.register(Annotation,AnnotationAdmin)# Import your custom models
admin.site.register(ArticleEdit,ArticleEditAdmin)# Import your custom models
admin.site.register(ArticleEditSummarySentence,ArticleEditSummarySentenceAdmin)# Import your custom models
