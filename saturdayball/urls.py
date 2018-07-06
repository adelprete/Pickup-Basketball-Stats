from django.conf.urls import include, url
from django.contrib import admin
from basketball import views as bviews
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views
from basketball.views import player

urlpatterns = [
        url(r'^group/(?P<group_id>\d+)/$',
            bviews.root,
            name='grouproot'),
        url(r'^$',TemplateView.as_view(template_name='base_angular.html'), name='go-to-group'),
        url(r'^ajax-standings/$',
            bviews.ajax_standings,
            name='ajax_standings'),
        url(r'^group/(?P<group_id>\d+)/records/$',
            bviews.records_home,
            name='records_home'),
        url(r'^group/(?P<group_id>\d+)/players/', include('basketball.urls.player')),
        url(r'^group/(?P<group_id>\d+)/games/', include('basketball.urls.game')),
        url(r'^api/', include('basketball.urls.api')),
        url(r'^accounts/', include('registration.backends.default.urls')),
        url(r'^admin/', include(admin.site.urls)),
        url(r'^accounts/login/$', auth_views.login, {'template_name': 'login.html'},name="login"),
        url(r'^logout/$', 'django.contrib.auth.views.logout',{'next_page': '/'},   name="logout"),
        url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
        url(r'^sitemap\.txt$', TemplateView.as_view(template_name='sitemap.txt', content_type='text/plain')),
        url(r'^.*/$', TemplateView.as_view(template_name='base_angular.html')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + staticfiles_urlpatterns()
