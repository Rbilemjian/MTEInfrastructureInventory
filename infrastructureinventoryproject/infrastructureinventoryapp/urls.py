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
    url(r'^applicationserver/edit/(?P<pk>\d+)/$', views.edit_application_server, name="edit-view"),
    url(r'^applicationserver/details/(?P<pk>\d+)/$', views.details_application_server, name="details-view"),
    url(r'^applicationserver/delete/(?P<pk>\d+)/$', views.delete_application_server, name="delete-view"),
    url(r'^applicationserver/import/confirm/$', views.confirm_import_application_server),
]