from django.conf.urls import *
from views import *

urlpatterns = patterns('',
                       (r'^$', hotel_matching),
                       (r'^irrelevant/$', irrelevant),
                       (r'^match/$', match),
                       (r'^save/$', savematches),
                       (r'^suggestions/$', hotel_matching)
)