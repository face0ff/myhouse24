from django.urls import path, include


from .views import Stat

urlpatterns = [
    path("", Stat.as_view(), name='admin'),


]