from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^upload/$', views.upload, name='upload'),
    url(r'^search_result/$', views.search_result, name='search_result'),
]