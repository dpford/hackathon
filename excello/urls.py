from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'excello.views.home', name='home'),
     url(r'^$', include('dashboard.urls')),
    url(r'^about/$', 'dashboard.views.about', name='about'),
    url(r'^login/$', 'dashboard.views.login', name='login'),
    url(r'^dashboard/$', 'dashboard.views.dashboard', name='dashboard'),
    url(r'^dashboard/$', 'dashboard.views.dashboard', name='dashboard'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url('', include('social.apps.django_app.urls', namespace='social'))
)