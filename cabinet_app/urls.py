from django.urls import path

from cabinet_app.views import *





urlpatterns = [

    # path("cabinet/", cabinet_stat.as_view(), name='cabinet'),
    path("cabinet/apartment_detail/<int:pk>", OwnerApartmentDetail.as_view(), name='owner_apartment_detail'),
    path("cabinet/invoice_list/", OwnerInvoiceList.as_view(), name='owner_invoice_list'),
    path("cabinet/invoice_detail/<int:pk>", OwnerInvoiceDetail.as_view(), name='owner_invoice_detail'),
    path("select_owner_invoice/", select_owner_invoice, name='select_owner_invoice'),
    path("cabinet/tariff_list/", OwnerTariffList.as_view(), name='owner_tariff_list'),
    path("cabinet/message_list/", OwnerMessageList.as_view(), name='owner_message_list'),
]