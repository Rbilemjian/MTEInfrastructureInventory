from django.conf.urls import url
from . import views
from django.contrib.auth.views import login, logout

urlpatterns = [

    # user registration urls
    url(r'^login/$', login, {'template_name': 'login.html'}),
    url(r'^logout/$', logout, {'template_name': 'logout.html', 'next_page': '/infrastructureinventory/login'}),

    #application server urls
    url(r'^applicationserver/$', views.view_application_servers),
    url(r'^applicationserver/add/$', views.create_application_server_form),
    url(r'^applicationserver/import/$', views.import_application_server),
]