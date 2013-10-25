from django.conf.urls import patterns, include, url
from django.contrib import admin
from main import views

admin.autodiscover()

urlpatterns = patterns('',

	(r'^messages/', include('postman.urls')),
    url(r'^about/', views.about, name='about'),  # about
    url(r'^badprofile/', views.badprofile, name='badprofile'),  # about
    url(r'^benefits/', views.benefits, name='benefits'),  # benefits
    url(r'^benefits_executives/', views.benefits_executives, name='benefits_executives'),  # benefits
    url(r'^benefits_managers/', views.benefits_managers, name='benefits_managers'),  # benefits
    url(r'^benefits_nurses/', views.benefits_nurses, name='benefits_nurses'),  # benefits
    url(r'^features/', views.features, name='features'),  # features
    url(r'^termsofservice/', views.termsofservice, name='termsofservice'),  # tos
    url(r'^privacy/', views.privacy, name='privacy'),  # privacy
    url(r'^contact/', views.contact, name='contact'),  # about
    url(r'^blog/', views.blog, name='blog'),  # blog
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.urls')),
    url(r'', include('main.urls')),

)
  