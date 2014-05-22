from django.conf.urls import patterns, include, url
from tastypie.api import Api
from appreq.resources import *
from survey.resources import SurveyResource

from django.contrib import admin
admin.autodiscover()

v1 = Api(api_name='v1')

v1.register(RequestResource())
v1.register(CoordinateResource())
v1.register(SurveyResource())
v1.register(MasterResource())
v1.register(DetailResource())
v1.register(MineralResource())

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mcs.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(v1.urls)),
)
