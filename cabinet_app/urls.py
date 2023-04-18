from django.urls import path

from cabinet_app.views import *





urlpatterns = [

    # path("cabinet/", cabinet_stat.as_view(), name='cabinet'),
    path("cabinet/apatrment_detail/<int:pk>", OwnerApartmentDetail.as_view(), name='owner_apartment_detail'),
]