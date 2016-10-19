from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^add_edit_room/$', views.room, name='room'),
    url(r'^(?P<room_id>[0-9]+)/remove_room/$', views.remove_room, name='remove_room'),
    url(r'^edit_room_name/$', views.edit_room_name, name='edit_room_name'),
]
