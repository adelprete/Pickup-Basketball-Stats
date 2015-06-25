from django.conf.urls import patterns, url, include

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('coms.core.base.views',
	url(r'^$',		'root',			name='root'),
}
