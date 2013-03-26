from django.http import HttpResponse
from django.template import Context, loader
from django.shortcuts import render, get_object_or_404
import json

from text_summarizer.models import *

def index(request,article_id):
    article = get_object_or_404(Article, pk=article_id)
    summarizer = Summarizer()
    paragraphs_with_edit_summary = article.paragraphs_with_edit_summary()
    #summary = summarizer.summarize(article.content)
    #summary = summarizer.summarize_using_cosine_similarity(article.content)
    summary = summarizer.summarize_using_cos_and_weights(article.content)
    summary_edit_sentences = []
    template = loader.get_template('index.html')
    context = Context({
        'summary': summary,
        'article_id':article_id,
        'title': article.title,
        'article_paragraphs_with_edit_summary': paragraphs_with_edit_summary,
        })
    return HttpResponse(template.render(context))

def save(request,article_id):
    article = get_object_or_404(Article, pk=article_id)
    original_paragraphs = article.paragraphs()
    edited_paragraphs = json.loads(request.GET.get('paragraphs'))
    print("#########################" + str(edited_paragraphs.keys()))
    for para_number in edited_paragraphs.keys():
        article_edit = ArticleEdit(article=article,paragraph_number=para_number,content=edited_paragraphs[para_number])
        article_edit.save()
    return HttpResponse('Success')

def summary_using_cosine_similarity(request,article_id):
    article = get_object_or_404(Article, pk=article_id)
    summarizer = Summarizer()
    summary_sentences = summarizer.summarize_using_cosine_similarity(article.content)
    return HttpResponse(json.dumps(summary_sentences), content_type="application/json")

def summary_using_weights(request,article_id):
    article = get_object_or_404(Article, pk=article_id)
    summarizer = Summarizer()
    summary_sentences = summarizer.summarize(article.content)
    return HttpResponse(json.dumps(summary_sentences), content_type="application/json")


def summary_using_cos_and_weights(request,article_id):
    article = get_object_or_404(Article, pk=article_id)
    summarizer = Summarizer()
    summary_sentences = summarizer.summarize_using_cos_and_weights(article.content)
    return HttpResponse(json.dumps(summary_sentences), content_type="application/json")
