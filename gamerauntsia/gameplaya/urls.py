from django.conf.urls import patterns, include, url
from gamerauntsia import settings

urlpatterns = patterns('',
    url(r'^$', 'gamerauntsia.gameplaya.views.index', name='gameplay_index'),
    url(r'^kategoriak/(?P<gaia>[-\w]+)/$', 'gamerauntsia.gameplaya.views.index', name='gameplay_gaia'),
    url(r'^jokalariak/(?P<user>[-\w]+)/$', 'gamerauntsia.gameplaya.views.index', name='gameplay_user'),
    url(r'^(?P<slug>[-\w]+)/$', 'gamerauntsia.gameplaya.views.gameplaya', name='gameplay'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',  
         {'document_root':     settings.MEDIA_ROOT}),
    )