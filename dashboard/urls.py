from django.conf.urls import patterns, url

urlpatterns = patterns('dashboard.views',
    url(r'^$', 'home', name='home'),
    url(r'^about/$', 'about', name='about'),
    url(r'^pricing/$', 'pricing', name='pricing'),
    url(r'^login/$', 'login', name='login'),
    url(r'^regster/$', 'register', name='register'),
)
