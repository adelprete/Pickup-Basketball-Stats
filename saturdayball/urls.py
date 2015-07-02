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

urlpatterns = [
	url(r'^$',	bviews.root,		name='root'),
	url(r'^(?P<id>\d+)/box_score/$',        bviews.box_score,            name='box_score'),
        url(r'^ajax-add-play/(?P<pk>[0-9]+)/$',        bviews.ajax_add_play,       name='ajax_add_play'),
        url(r'^delete-play/(?P<pk>[0-9]+)/$',        bviews.delete_play,       name='delete_play'),
        url(r'^admin/', include(admin.site.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + staticfiles_urlpatterns()
