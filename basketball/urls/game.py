from django.conf.urls import include, url
from django.urls import re_path
from basketball.views import game as gviews
from django.contrib.auth.decorators import login_required
from basketball.views.game import PlaysViewSet
from rest_framework import renderers

plays_list = PlaysViewSet.as_view({
    'get': 'list',
})


urlpatterns = [
	#url(r'^$',                 gviews.games_home,       name='games_home'),
	re_path(r'^(?P<id>\d+)/box-score/$',        gviews.box_score,            name='box_score'),
	re_path(r'^(?P<game_id>\d+)/play/(?P<play_id>[0-9]+)/$',  login_required(gviews.PlayByPlayFormView.as_view()), name='playbyplay_detail'),
	re_path(r'^new-game/$',        gviews.game_basics,            name='create_game'),
	re_path(r'^(?P<game_id>\d+)/edit-game/$',        gviews.game_basics, name='edit_game'),
	re_path(r'^recap/(?P<game_id>\d+)/$',  gviews.recap, name='recap'),

	re_path(r'^ajax-add-play/(?P<pk>[0-9]+)/$',        gviews.ajax_add_play,       name='ajax_add_play'),
	re_path(r'ajax-filter-plays/(?P<pk>[0-9]+)/$',      gviews.ajax_filter_plays,   name="ajax_filter_plays"),
	re_path(r'^delete-play/(?P<pk>[0-9]+)/$',        gviews.delete_play,       name='delete_play'),
	re_path(r'^(?P<game_id>\d+)/export_plays/$',        gviews.export_plays,       name='export_plays'),
]
