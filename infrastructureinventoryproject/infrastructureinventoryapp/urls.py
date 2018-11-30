from django.conf.urls import url
from . import views, infoblox_views
from django.contrib.auth.views import login, logout

urlpatterns = [

    # user registration urls
    url(r'^login/$', login, {'template_name': 'login.html'}),
    url(r'^logout/$', logout, {'template_name': 'logout.html', 'next_page': '/infrastructureinventory/login'}),

    #information viewing urls
    url(r'^applicationserver/$', views.view_application_servers),
    url(r'^applicationserver/details/(?P<pk>\d+)/$', views.details_application_server, name="details-view"),
    #
    # #form urls
    # url(r'^applicationserver/add/$', views.create_application_server_form),
    # url(r'^applicationserver/edit/(?P<pk>\d+)/$', views.edit_application_server, name="edit-view"),
    #
    # #import urls
    # url(r'^applicationserver/import/$', views.import_application_server),
    # url(r'^applicationserver/import/confirm/$', views.confirm_import_application_server),
    #
    # #delete urls
    # url(r'^applicationserver/delete/confirm/(?P<pk>\d+)/$', views.application_server_delete_confirm, name="delete-confirmation-view"),
    # url(r'^applicationserver/delete/(?P<pk>\d+)/$', views.delete_application_server, name="delete-view"),
    #
    # url(r'^applicationserver/filterprofile/delete/confirm/(?P<pk>\d+)/$', views.filter_profile_delete_confirm, name="filter-profile-delete-confirm-view"),
    # url(r'^applicationserver/filterprofile/delete/(?P<pk>\d+)/$', views.filter_profile_delete, name="filter-profile-delete"),
    #
    # #search urls
    # url(r'^applicationserver/search', views.search_application_server, name="search-view"),
    #
    # #filter profile urls
    # url(r'^applicationserver/filteredlist/(?P<pk>\d+)/$', views.filtered_list, name="filtered-list-view"),
    # url(r'^applicationserver/filterprofile/$', views.filter_profile, name="filter-profile-view"),
    # url(r'^applicationserver/filterform/$', views.filter_profile_form),
    # url(r'^applicationserver/filterprofile/edit/(?P<pk>\d+)/$', views.filter_profile_edit, name="filter-profile-detail-view"),

    #infoblox urls
    url(r'^applicationserver/infoblox', infoblox_views.infoblox)
]