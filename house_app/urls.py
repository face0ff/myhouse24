from django.urls import path

from house_app import views
from house_app.views import *

urlpatterns = [

    path("admin/houses_list/", HousesList.as_view(), name='houses_list'),
    path("admin/house/<int:pk>", HouseDetail.as_view(), name='house_detail'),
    path("admin/house/create/", HouseCreate.as_view(), name='house_create'),
    path("admin/house/delete/<int:pk>", views.house_delete, name='house_delete'),
    path("admin/house/update/<int:pk>", HouseUpdate.as_view(), name='house_update'),
    path("select_user/", select_user, name='select_user'),

    path("admin/apartment_list/", ApartmentsList.as_view(), name='apartments_list'),
    path("admin/apartment/<int:pk>", ApartmentDetail.as_view(), name='apartment_detail'),
    path("admin/apartment/create/", ApartmentCreate.as_view(), name='apartment_create'),
    path("admin/apartment/delete/<int:pk>", views.apartment_delete, name='apartment_delete'),
    path("admin/apartment/update/<int:pk>", ApartmentUpdate.as_view(), name='apartment_update'),
    path("select_house/", select_house, name='select_house'),

    path("admin/requests_list/", RequestsList.as_view(), name='requests_list'),
    path("admin/request/<int:pk>", RequestDetail.as_view(), name='request_detail'),
    path("admin/request/create/", RequestCreate.as_view(), name='request_create'),
    path("admin/request/update/<int:pk>", RequestUpdate.as_view(), name='request_update'),
    path("admin/request/delete/<int:pk>", views.request_delete, name='request_delete'),
    path("select_apart/", select_apart, name='select_apart'),

    path("admin/messages_list/", MessagesList.as_view(), name='messages_list'),
    path("admin/message/<int:pk>", MessageDetail.as_view(), name='message_detail'),
    path("admin/message/create/", MessageCreate.as_view(), name='message_create'),
    path("admin/message/delete/<int:pk>", views.message_delete, name='message_delete'),
    path("message_select_house/", message_select_house, name='message_select_house'),
    path("delete_selected_messages/", delete_selected_messages, name='delete_selected_messages'),

    path("admin/account/", AccountsList.as_view(), name='accounts_list'),
    path("admin/account/<int:pk>", AccountDetail.as_view(), name='account_detail'),
    path("admin/account/create/", AccountCreate.as_view(), name='account_create'),
    path("admin/account/update/<int:pk>", AccountUpdate.as_view(), name='account_update'),
    path("admin/account/delete/<int:pk>", views.account_delete, name='account_delete'),
    path("select_account/", select_account, name='select_account'),

    path("admin/invoices_list/", InvoicesList.as_view(), name='invoices_list'),
    path("admin/invoice/create/", InvoiceCreate.as_view(), name='invoice_create'),
    path("admin/invoice/detail/<int:pk>", InvoiceDetail.as_view(), name='invoice_detail'),
    path("admin/invoice/update/<int:pk>", InvoiceUpdate.as_view(), name='invoice_update'),
    path("admin/invoice/delete/<int:pk>", views.invoice_delete, name='invoice_delete'),
    path("select_invoices/", select_invoices, name='select_invoices'),
    path("delete_selected_invoice/", delete_selected_invoice, name='delete_selected_invoice'),
    path("invoice_unit/", invoice_unit, name='invoice_unit'),

    path("admin/transfers_list/", TransfersList.as_view(), name='transfers_list'),
    path("admin/transfer/create/", TransferCreate.as_view(), name='transfer_create'),
    path("admin/transfer/detail/<int:pk>", TransferDetail.as_view(), name='transfer_detail'),
    path("admin/transfer/update/<int:pk>", TransferUpdate.as_view(), name='transfer_update'),
    path("admin/transfer/delete/<int:pk>", views.transfer_delete, name='transfer_delete'),
    path("select_transfers/", select_transfers, name='select_transfers'),



]