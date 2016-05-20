from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$|^board/', views.index, name='index'),
    url(r'items', views.get_items, name='get_items')
]
