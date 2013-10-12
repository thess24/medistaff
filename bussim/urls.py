from django.conf.urls import patterns, include, url
from django.contrib import admin
from main import views

admin.autodiscover()

urlpatterns = patterns('',

	(r'^messages/', include('postman.urls')),
    url(r'^about/', views.about, name='about'),  # about
    url(r'^badprofile/', views.badprofile, name='badprofile'),  # about
    url(r'^benefits/', views.benefits, name='benefits'),  # about
    url(r'^contact/', views.contact, name='contact'),  # about
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.urls')),
    url(r'', include('main.urls')),

)
  