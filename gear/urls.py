from django.conf.urls import url
from . import views

app_name = 'gear'
urlpatterns = [
    url(r'^list/', views.gear_list, name='list'),
    url(r'^add/', views.add, name='add'),
    url(r'^edit/', views.edit, name='edit'),
    url(r'^delete/', views.delete, name='delete'),
]
