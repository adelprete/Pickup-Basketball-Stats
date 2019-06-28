from django.conf.urls import include, url
from django.urls import re_path
from base.views import (
    CreateUserView, GroupViewSet, current_user, verify_group_admin,
    group_seasons, MemberPermissionViewSet, MemberInviteViewSet,
    ContactViewSet
)
from basketball.views import game as gviews, player as pviews, team as tviews
from django.contrib.auth.decorators import login_required
from basketball.views.game import (
    PlaysViewSet, GameViewSet, DailyStatlineViewSet, PlayerViewSet,
    SeasonStatlineViewSet, calculate_statlines, game_box_score,
    game_adv_box_score, export_plays, StatlineViewSet, AwardViewSet
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

"""
team_details = tviews.TeamViewSet.as_view({
    'get': 'retrieve',
})

team_list = tviews.TeamViewSet.as_view({
    'get': 'list'
})
"""

player_details = PlayerViewSet.as_view({
    'get': 'retrieve',
    'post': 'update'
})

player_list = PlayerViewSet.as_view({
    'get': 'list'
})

award_list = AwardViewSet.as_view({
    'get': 'list'
})


router = routers.SimpleRouter()
router.register(r'awards', AwardViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'contacts', ContactViewSet)
router.register(r'daily-statlines', DailyStatlineViewSet)
router.register(r'member-permissions', MemberPermissionViewSet)
router.register(r'member-invite', MemberInviteViewSet)
router.register(r'players', PlayerViewSet)
router.register(r'teams', tviews.TeamViewSet)
router.register(r'statlines', StatlineViewSet)
router.register(r'season-statlines', SeasonStatlineViewSet, 'SeasonStatline')

urlpatterns = [
	#API
    re_path(r'^user/current/', current_user),
    re_path(r'^user/create/', CreateUserView.as_view()),
    re_path(r'^players/(?P<player_id>[0-9]+)/overall_averages$',  pviews.player_overall_averages),
    re_path(r'^players/(?P<player_id>[0-9]+)/overall_totals$',  pviews.player_overall_totals),
    re_path(r'^players/(?P<player_id>[0-9]+)/overall_adv_totals$',  pviews.player_overall_adv_totals),
    re_path(r'^players/(?P<player_id>[0-9]+)/overall_per100$',  pviews.player_overall_per100),
    re_path(r'^players/(?P<player_id>[0-9]+)/overall_adv_per100$',  pviews.player_overall_adv_per100),
    #re_path(r'^teams/groupid/(?P<group_id>[0-9]+)/$',  team_list),
    #re_path(r'^teams/(?P<pk>[0-9]+)/$',  team_details),
	re_path(r'^plays/$',  plays_list),
    re_path(r'^plays/(?P<pk>[0-9]+)/$',  plays_details),
    re_path(r'^games/groupid/(?P<group_id>[0-9]+)/$',  game_list),
    re_path(r'^games/(?P<pk>[0-9]+)/$',  game_details),
    re_path(r'^games/(?P<pk>[0-9]+)/export/$', export_plays),
    re_path(r'^games/(?P<pk>[0-9]+)/box-score/$',  game_box_score),
    re_path(r'^games/(?P<pk>[0-9]+)/adv-box-score/$',  game_adv_box_score),
    re_path(r'^games/(?P<pk>[0-9]+)/calculate-statlines/$',  calculate_statlines),
    re_path(r'^group/(?P<pk>[0-9]+)/verify-admin/$',  verify_group_admin),
    re_path(r'^group/(?P<pk>[0-9]+)/seasons/$',  group_seasons),
    re_path(r'^group/(?P<group_id>[0-9]+)/players/$',  group_seasons),


]

urlpatterns += router.urls
