from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^travels$', views.travels),
    url(r'^travels/(?P<id>\d+)$', views.itinerary),
    url(r'^add_trip$', views.add_trip),
    url(r'^process_trip$', views.process_trip),
    url(r'^delete/(?P<id>\d+)$', views.delete),
    url(r'^join/(?P<trip_id>\d+)$', views.buddy)
]
