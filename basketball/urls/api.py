from django.conf.urls import include, url
from basketball.views import game as gviews
from django.contrib.auth.decorators import login_required
from basketball.views.game import PlaysViewSet, GameViewSet
from rest_framework import renderers

plays_list = PlaysViewSet.as_view({
    'get': 'list',
    'post': 'create',
    'delete': 'destroy'
})

plays_details = PlaysViewSet.as_view({
    'delete': 'destroy',
    'get': 'retrieve'
})

game_details = GameViewSet.as_view({
    'get': 'retrieve',
})


urlpatterns = [
	#API
	url(r'^plays/$',  plays_list),
    url(r'^plays/(?P<pk>[0-9]+)/$',  plays_details),
    url(r'^games/(?P<pk>[0-9]+)/$',  game_details),
]
