from django.conf.urls import include, url
from django.urls import re_path
from django.contrib import admin, auth
from basketball import views as bviews
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views
from basketball.views import player

urlpatterns = [
        re_path(r'^group/(?P<group_id>\d+)/$',
            bviews.root,
            name='grouproot'),
        re_path(r'^$',TemplateView.as_view(template_name='base_angular.html'), name='go-to-group'),
        re_path(r'^ajax-standings/$',
            bviews.ajax_standings,
            name='ajax_standings'),
        re_path(r'^group/(?P<group_id>\d+)/records/$',
            bviews.records_home,
            name='records_home'),
        re_path(r'^group/(?P<group_id>\d+)/players/', include('basketball.urls.player')),
        re_path(r'^group/(?P<group_id>\d+)/games/', include('basketball.urls.game')),
        re_path(r'^api/', include('basketball.urls.api')),
        re_path(r'^accounts/', include('registration.backends.default.urls')),
        re_path(r'^admin/', admin.site.urls),
        re_path(r'^accounts/login/$', auth_views.login, {'template_name': 'login.html'}, name="login"),
        re_path(r'^logout/$', auth.views.logout, {'next_page': '/'}, name="logout"),
        re_path(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
        re_path(r'^sitemap\.txt$', TemplateView.as_view(template_name='sitemap.txt', content_type='text/plain')),
        re_path(r'^.*/$', TemplateView.as_view(template_name='base_angular.html')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + staticfiles_urlpatterns()
