from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'excello.views.home', name='home'),
     url(r'^$', include('dashboard.urls')),
    url(r'^about/$', 'dashboard.views.about', name='about'),
    url(r'^pricing/$', 'dashboard.views.pricing', name='pricing'),
    url(r'^login/$', 'dashboard.views.login', name='login'),
    url(r'^register/$', 'dashboard.views.register', name='register'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatters += patters('',
    (r'^static/(?P<path>.*)$', 'django.contrib.staticfiles.views', {'document_root': settings.STATIC_ROOT}),
    )