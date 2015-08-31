"""saturdayball URL Configuration

Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from basketball import views as bviews
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views
urlpatterns = [
	url(r'^$',	bviews.root,		name='root'),
        url(r'^ajax-add-play/(?P<pk>[0-9]+)/$',        bviews.ajax_add_play,       name='ajax_add_play'),
        url(r'ajax-filter-plays/(?P<pk>[0-9]+)/$',      bviews.ajax_filter_plays,   name="ajax_filter_plays"),
        url(r'^delete-play/(?P<pk>[0-9]+)/$',        bviews.delete_play,       name='delete_play'),
        
        url(r'^players-home/$',                 bviews.players_home,       name='players_home'),
        url(r'^player/(?P<id>[0-9]+)/$',                 bviews.player,       name='player_page'),
        url(r'^player/(?P<id>[0-9]+)/edit-player/$', bviews.player_basics,       name='edit_player'),
        url(r'^player/new-player$',     bviews.player_basics,       name='create_player'),
        
	url(r'^games-home/(?P<id>\d+)/box-score/$',        bviews.box_score,            name='box_score'),
        url(r'^games-home/(?P<game_id>\d+)/play/(?P<play_id>[0-9]+)/$',  bviews.PlayByPlayFormView.as_view(), name='playbyplay_detail'),
        url(r'^games-home/new-game/$',        bviews.game_basics,            name='create_game'),
        url(r'^games-home/(?P<game_id>\d+)/edit-game/$',        bviews.game_basics, name='edit_game'),
        url(r'^games-home/recap/(?P<game_id>\d+)/$',  bviews.recap, name='recap'),
        url(r'^games-home/$',                 bviews.games_home,       name='games_home'),
        
        url(r'^leaderboard-home/$',     bviews.leaderboard_home,    name='leaderboard_home'),
        
        url(r'^admin/', include(admin.site.urls)),
        url(r'^accounts/login/$', auth_views.login, {'template_name': 'login.html'},name="login"),
        url(r'^logout/$', 'django.contrib.auth.views.logout',{'next_page': '/'},   name="logout"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + staticfiles_urlpatterns()
