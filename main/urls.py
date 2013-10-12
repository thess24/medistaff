from django.conf.urls import patterns, url
from main import views

 

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),    
    # url(r'^systemsettings/$', views.systemsettings, name='systemsettings'),  # nurse select/filter
    url(r'^(?P<systempass>.+)/(?P<hospitalpass>.+)/(?P<unitpass>.+)/census/$', views.addunitcensus, name='addunitcensus'),  # hospital overview
    url(r'^(?P<systempass>.+)/(?P<hospitalpass>.+)/(?P<unitpass>.+)/schedule/$', views.schedule, name='schedule'),  # unit schedule
    url(r'^(?P<systempass>.+)/(?P<hospitalpass>.+)/(?P<unitpass>.+)/addopenshift/$', views.addopenshift, name='addopenshift'),  # unit schedule
    url(r'^(?P<systempass>.+)/(?P<hospitalpass>.+)/addunit/$', views.addunit, name='addunit'),
    url(r'^(?P<systempass>.+)/(?P<hospitalpass>.+)/census/$', views.addcensus, name='addcensus'),  # hospital overview
    url(r'^(?P<systempass>.+)/(?P<hospitalpass>.+)/budget/$', views.addbudget, name='addbudget'),  # hospital overview
    url(r'^(?P<systempass>.+)/user/(?P<username>.+)/$', views.profile, name='profile'),  # nurse profile page
    url(r'^(?P<systempass>.+)/(?P<hospitalpass>.+)/(?P<unitpass>.+)/$', views.unit, name='unit'),  # unit overview
    url(r'^(?P<systempass>.+)/openshift/$', views.openshift, name='openshift'),  # open shift marketplace
    url(r'^(?P<systempass>.+)/systemsettings/$', views.systemsettings, name='systemsettings'),  # system settings
    url(r'^(?P<systempass>.+)/addhospital/$', views.addhospital, name='addhospital'),  # add hospital
    url(r'^(?P<systempass>.+)/addopenshift/$', views.openshiftindex, name='openshiftindex'),  # openshift adding index
    url(r'^(?P<systempass>.+)/inputdates/$', views.inputdates, name='inputdates'),  # add schedule
    url(r'^(?P<systempass>.+)/nursefilter/$', views.nursefilter, name='nursefilter'),  # add hospital
    url(r'^(?P<systempass>.+)/settings/$', views.settings, name='settings'),  # nurse settings and home
    url(r'^(?P<systempass>.+)/home/$', views.home, name='home'),  # nurse home - lists hours you are working
    url(r'^(?P<systempass>.+)/(?P<hospitalpass>.+)/$', views.hospital, name='hospital'),  # hospital overview
    url(r'^(?P<systempass>.+)/$', views.systemoverview, name='systemoverview'),  # system overview

)



###########################

#### HIGH PRIORITY--Key Featurns

# make system for users to register to a certain system and get verified-- key maps to system
# make unit tables work in hopsital dashboard- SQL
# javascript scheduler

# make frontend sales pages
# figure out displaying images

# add agency as person
# do page to input schedules
# work on census prediction/forcasting



#### MID PRIORITY

# add data page- to compare and sort through data of different periods
# export schedule to pdf, excel
# add south




#### Pages to add

# about
# contact
# why buy--value for corporate, nurses, managers
# overview of features

# data pull
# page for nurses to list hours
# recent events



#### Bonus Features

# text to nurse



###########################

# problems



###########################

# think about strat and features, benefits... better define
# makes scheduling easy
# flex scheduling
# helps reduce cost through worker mix, better scheduling, less premium labor
# tracks if you are on labor budget or not?
# needs some metrics to compare against other hospitals
# lasting competitive advantage?






############################

# Questions?????

# How does Agency work? Do the workers have to get approved? Do they work for a day or for a few weeks?
# How is census reported in the hospital? By unit? How is HPPD calculated? Who reports it?



    # url(r'^inbox/(?:(?P<option>'+OPTIONS+')/)?$', InboxView.as_view(), name='postman_inbox'),
    # url(r'^sent/(?:(?P<option>'+OPTIONS+')/)?$', SentView.as_view(), name='postman_sent'),
    # url(r'^archives/(?:(?P<option>'+OPTIONS+')/)?$', ArchivesView.as_view(), name='postman_archives'),
    # url(r'^trash/(?:(?P<option>'+OPTIONS+')/)?$', TrashView.as_view(), name='postman_trash'),
    # url(r'^write/(?:(?P<recipients>[\w.@+-:]+)/)?$', WriteView.as_view(), name='postman_write'),
    # url(r'^reply/(?P<message_id>[\d]+)/$', ReplyView.as_view(), name='postman_reply'),
    # url(r'^view/(?P<message_id>[\d]+)/$', MessageView.as_view(), name='postman_view'),
    # url(r'^view/t/(?P<thread_id>[\d]+)/$', ConversationView.as_view(), name='postman_view_conversation'),
    # url(r'^archive/$', ArchiveView.as_view(), name='postman_archive'),
    # url(r'^delete/$', DeleteView.as_view(), name='postman_delete'),
    # url(r'^undelete/$', UndeleteView.as_view(), name='postman_undelete'),
    # (r'^$', RedirectView.as_view(url='inbox/')),