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
from basketball.views import player


urlpatterns = [
	url(r'^$',	bviews.root,		name='root'),
        url(r'^ajax-standings/$',        bviews.ajax_standings,       name='ajax_standings'),

        url(r'^leaderboard/$',     bviews.leaderboard_home,    name='leaderboard_home'),
        
        url(r'^players/', include('basketball.urls.player')),
        url(r'^games/', include('basketball.urls.game')),
        
        url(r'^admin/', include(admin.site.urls)),
        url(r'^accounts/login/$', auth_views.login, {'template_name': 'login.html'},name="login"),
        url(r'^logout/$', 'django.contrib.auth.views.logout',{'next_page': '/'},   name="logout"),
        
        url(r'^lazy_tags/', include('lazy_tags.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + staticfiles_urlpatterns()
