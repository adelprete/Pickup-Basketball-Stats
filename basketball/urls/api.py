from django.conf.urls import include, url
from base.views import (
    CreateUserView, GroupViewSet, current_user, verify_group_admin,
    group_seasons, MemberPermissionViewSet, MemberInviteViewSet
)
from basketball.views import game as gviews
from django.contrib.auth.decorators import login_required
from basketball.views.game import (
    PlaysViewSet, GameViewSet,DailyStatlineViewSet, PlayerViewSet,
    SeasonStatlineViewSet, calculate_statlines, game_box_score,
    game_adv_box_score, export_plays
    )
from rest_framework import renderers, routers

plays_list = PlaysViewSet.as_view({
    'get': 'list',
    'post': 'create',
    'delete': 'destroy'
})

plays_details = PlaysViewSet.as_view({
    'delete': 'destroy',
    'get': 'retrieve',
    'post': 'update'
})

game_details = GameViewSet.as_view({
    'get': 'retrieve',
})

game_list = GameViewSet.as_view({
    'get': 'list'
})

player_list = PlayerViewSet.as_view({
    'get': 'list'
})


router = routers.SimpleRouter()
router.register(r'groups', GroupViewSet)
#router.register(r'statlines', StatlineViewSet)
router.register(r'daily-statlines', DailyStatlineViewSet)
router.register(r'member-permissions', MemberPermissionViewSet)
router.register(r'member-invite', MemberInviteViewSet)
router.register(r'season-statlines', SeasonStatlineViewSet)

urlpatterns = [
	#API
    url(r'^user/current', current_user),
    url(r'^user/create', CreateUserView.as_view()),
	url(r'^plays/$',  plays_list),
    url(r'^plays/(?P<pk>[0-9]+)/$',  plays_details),
    url(r'^players/(?P<group_id>[0-9]+)/$',  player_list),
    url(r'^games/groupid/(?P<group_id>[0-9]+)/$',  game_list),
    url(r'^games/(?P<pk>[0-9]+)/$',  game_details),
    url(r'^games/(?P<pk>[0-9]+)/export$', export_plays),
    url(r'^games/(?P<pk>[0-9]+)/box-score$',  game_box_score),
    url(r'^games/(?P<pk>[0-9]+)/adv-box-score$',  game_adv_box_score),
    url(r'^games/(?P<pk>[0-9]+)/calculate-statlines/$',  calculate_statlines),
    url(r'^group/(?P<pk>[0-9]+)/verify-admin/$',  verify_group_admin),
    url(r'^group/(?P<pk>[0-9]+)/seasons/$',  group_seasons)
]

urlpatterns += router.urls
