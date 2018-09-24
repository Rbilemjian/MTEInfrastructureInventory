from django.conf.urls import url
from . import views
from django.contrib.auth.views import login, logout

urlpatterns = [
    url(r'^$', views.home),

# user registration urls
    url(r'^login/$', login, {'template_name': 'login.html'}),
    url(r'^logout/$', logout, {'template_name': 'logout.html'}),
]