from django.conf.urls import url
from . import views

app_name = 'gear'
urlpatterns = [
    url(r'^list/', views.gear_list, name='list'),
    url(r'^add/', views.add, name='add'),
    url(r'^edit/(?P<gear_id>\d+)/', views.edit, name='edit'),
    url(r'^details/(?P<gear_id>\d+)/', views.details, name='details'),
    url(r'^delete/(?P<gear_id>\d+)/', views.delete, name='delete'),
]
