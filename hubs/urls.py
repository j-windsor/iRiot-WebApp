from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^manage/$', views.manage, name='manage'),
    url(r'^change_name/$', views.change_name, name='change_name'),
    url(r'^change_room/$', views.change_room, name='change_room'),
    url(r'^(?P<hub_id>[0-9]+)/remove_hub/$', views.remove_hub, name='remove_hub'),
]
