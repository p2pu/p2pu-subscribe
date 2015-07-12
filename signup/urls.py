from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^signup/$', 'signup.views.signup', name='signup'),
    url(r'^success/$', 'signup.views.success', name='signup_success'),
    url(r'^api/signup/$', 'signup.views.signup_ajax', name='signup_ajax'),
    url(r'^count/(?P<sequence>[\w-]+)/$', 'signup.views.count', name='signup_count'),
    url(r'^export/(?P<sequence>[\w-]+)/$', 'signup.views.export', name='signup_export'),
)
