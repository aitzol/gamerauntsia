from django.conf.urls import patterns, include, url
from django.conf import settings

urlpatterns = patterns('',
    url(r'^$', 'gamerauntsia.jokoa.views.index', name='game_index'),
    url(r'^(?P<slug>[-\w]+)$', 'gamerauntsia.jokoa.views.jokoa', name='game'),
)

if getattr(settings, 'DEBUG', False):
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': getattr(settings, 'MEDIA_ROOT', '')}),
    )
