from django.urls import path

from services_app import views
from services_app.views import *

urlpatterns = [
    path("show_unit_service/", views.show_unit_service, name='show_unit_service'),

    path("admin/services/", ServicesAdmin.as_view(), name='services'),
    path("admin/tariffs/", TariffsList.as_view(), name='tariffs'),
    path("admin/tariff/<int:pk>", TariffDetail.as_view(), name='tariff_detail'),
    path("admin/tariff/create/", TariffCreate.as_view(), name='tariff_create'),
    path("admin/tariff/create/<int:pk>", TariffCreate.as_view(), name='tariff_create'),
    path("admin/tariff/update/<int:pk>", TariffUpdate.as_view(), name='tariff_update'),
    path("admin/tariff/delete/<int:pk>", views.tariff_delete, name='tariff_delete'),

    path("admin/requisite/", Requisite.as_view(), name='requisite'),

    path("admin/item/", ItemList.as_view(), name='items'),
    path("admin/item/create/", ItemCreate.as_view(), name='item_create'),
    path("admin/item/update/<int:pk>", ItemUpdate.as_view(), name='item_update'),
    path("admin/item/delete/<int:pk>", views.item_delete, name='item_delete'),

    path("admin/meter_list/", MeterList.as_view(), name='meter_list'),
    path("admin/meter_apartment_list/", MeterApartmentList.as_view(), name='meter_apartment_list'),
    path("admin/meter/<int:pk>", MeterDetail.as_view(), name='meter_detail'),
    path("admin/meter/create/", MeterCreate.as_view(), name='meter_create'),
    path("admin/meter/create/<int:pk>", MeterCreate.as_view(), name='meter_create'),
    path("admin/meter/update/<int:pk>", MeterUpdate.as_view(), name='meter_update'),
    path("admin/meter/delete/<int:pk>", views.meter_delete, name='meter_delete'),
    path("select_field/", select_field, name='select_field'),



]