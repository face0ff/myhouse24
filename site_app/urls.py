from django.urls import path

from site_app import views
from site_app.views import MainAdmin, ContactsAdmin, InfoAdmin, del_img, ServiceAdmin, IndexSite, InfoSite, \
    ServiceSite, ContactsSite

urlpatterns = [
    path('', IndexSite.as_view(), name='index'),
    path("info/", InfoSite.as_view(), name='info'),
    path("service/", ServiceSite.as_view(), name='service'),
    path("contacts/", ContactsSite.as_view(), name='contacts'),
    path("admin/main_page/", MainAdmin.as_view(), name='main_page'),
    path("admin/contacts_page/", ContactsAdmin.as_view(), name='contacts_page'),
    path("admin/info_page/", InfoAdmin.as_view(), name='info_page'),
    path("admin/service_page/", ServiceAdmin.as_view(), name='service_page'),
    path("admin/info_page/del/<type>-<id>", views.del_img, name='del_img')

]
