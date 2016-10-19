from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^update/$', views.update, name='update'),
    url(r'^new/$', views.new, name='new'),
    url(r'^(?P<room_id>[0-9]+)/manage/$', views.manage, name='manage'),
    url(r'^(?P<room_id>[0-9]+)/remove_device/(?P<device_id>[0-9]+)$', views.remove_device, name='remove_device'),
    url(r'^(?P<function_id>[0-9]+)/send_function/$', views.send_function, name='send_function'),
]
