from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
     url(r'^article/(?P<article_id>\d+)/$', 'text_summarizer.views.index', name='home'),
     url(r'^article/(?P<article_id>\d+)/summary_using_weights$', 'text_summarizer.views.summary_using_weights', name='weight_summary'),
     url(r'^article/(?P<article_id>\d+)/summary_using_cosine_and_weights$', 'text_summarizer.views.summary_using_cos_and_weights', name='summary_using_cos_and_weights'),
     url(r'^article/(?P<article_id>\d+)/summary_using_cosine_similarity$', 'text_summarizer.views.summary_using_cosine_similarity', name='cosine_summary'),
     url(r'^article/(?P<article_id>\d+)/edit/save/', 'text_summarizer.views.save', name='save_edit'),
    # url(r'^xpertSummary/', include('xpertSummary.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
     url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
)
urlpatterns += staticfiles_urlpatterns()
