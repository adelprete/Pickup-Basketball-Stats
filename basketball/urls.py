from django.conf.urls import patterns, url, include

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('basketball.views',
	url(r'^$',		'root',			name='root'),
}
