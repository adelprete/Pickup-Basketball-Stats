from django.conf.urls import include, url
from django.contrib import admin
from basketball import views as bviews
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views
from basketball.views import player

urlpatterns = [
        url(r'^$',	bviews.root,		name='root'),
        url(r'^ajax-standings/$',       bviews.ajax_standings,          name='ajax_standings'),
        url(r'^leaderboard/$',          bviews.leaderboard_home,        name='leaderboard_home'),
        url(r'^records/$',              bviews.records_home,            name='records_home'),
        url(r'^players/', include('basketball.urls.player')),
        url(r'^games/', include('basketball.urls.game')),
        url(r'^api/', include('basketball.urls.api')),
        url(r'^accounts/', include('registration.backends.default.urls')),
        url(r'^admin/', include(admin.site.urls)),
        url(r'^accounts/login/$', auth_views.login, {'template_name': 'login.html'},name="login"),
        url(r'^logout/$', 'django.contrib.auth.views.logout',{'next_page': '/'},   name="logout"),
        url(r'^.*/$', TemplateView.as_view(template_name='base_angular.html')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + staticfiles_urlpatterns()
