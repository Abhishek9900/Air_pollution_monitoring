from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'monitor/$', views.monitor, name='monitor'),
    url(r'node/$', views.node, name='node'),
]