from django.conf.urls import include, url
from basketball.views import player as pviews

urlpatterns = [
	url(r'^$',									pviews.players_home,	name='players_home'),
	url(r'^(?P<id>[0-9]+)/$',					pviews.player_page,     name='player_page'),
	url(r'^(?P<id>[0-9]+)/edit-player/$',		pviews.player_basics,   name='edit_player'),
	url(r'^new-player$',						pviews.player_basics,   name='create_player'),
        url(r'^game-log/$',						pviews.ajax_game_log,   name='ajax_player_game_log'),
]
