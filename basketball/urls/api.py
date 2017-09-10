from django.conf.urls import include, url
from base.views import CreateUserView, GroupViewSet, current_user
from basketball.views import game as gviews
from django.contrib.auth.decorators import login_required
from basketball.views.game import PlaysViewSet, GameViewSet, calculate_statlines
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

router = routers.SimpleRouter()
router.register(r'groups', GroupViewSet)


urlpatterns = [
	#API
    url(r'^user/current', current_user),
    url(r'^user/create', CreateUserView.as_view()),
	url(r'^plays/$',  plays_list),
    url(r'^plays/(?P<pk>[0-9]+)/$',  plays_details),
    url(r'^games/(?P<pk>[0-9]+)/$',  game_details),
    url(r'^games/(?P<pk>[0-9]+)/calculate-statlines/$',  calculate_statlines),
]

urlpatterns += router.urls
