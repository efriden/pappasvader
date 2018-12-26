"""
Definition of urls for pappasvader.
"""

from django.conf.urls import include, url
from TestApp.widgets import Weather
from TestApp.widgets import Forecast
from TestApp.widgets import Trello
from TestApp.widgets import Sun
from dashing.utils import router

import TestApp.views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', pappasvader.views.home, name='home'),
    # url(r'^pappasvader/', include('pappasvader.pappasvader.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

	url(r'^', include(router.urls)),

	url(r'^weather/', Weather.as_view(), name='weather_widget'),
	url(r'^forecast/', Forecast.as_view(), name='forecast_widget'),
	url(r'^trello/', Trello.as_view(), name='trello_widget'),
	url(r'^sun/', Sun.as_view(), name='sun_widget'),

	#url(r'^index$', TestApp.views.index, name='index'),
	
]
