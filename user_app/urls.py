from django.urls import path

from user_app import views
from user_app.views import *

urlpatterns = [
    path('roles/', Roles.as_view(), name='roles'),
    path("admin/users_list/", UsersList.as_view(), name='users_list'),
    path("admin/user/<int:pk>", UserDetail.as_view(), name='user_detail'),
    path("admin/user/create/", UserCreate.as_view(), name='user_create'),
    path("admin/user/update/<int:pk>", UserUpdate.as_view(), name='user_update'),
    path("admin/user/delete/<int:pk>", views.user_delete, name='user_delete'),
    # path('admin/user/', get_data, name='get_data'),


    path("admin/owners_list/", OwnersList.as_view(), name='owners_list'),
    path("admin/owner/<int:pk>", OwnerDetail.as_view(), name='owner_detail'),
    path("admin/owner/create/", OwnerCreate.as_view(), name='owner_create'),
    path("admin/owner/update/<int:pk>", OwnerUpdate.as_view(), name='owner_update'),
    path("admin/owner/delete/<int:pk>", views.owner_delete, name='owner_delete'),
    path("admin/owner_invite/", OwnerInvite.as_view(), name='owner_invite'),

    path('users/login_admin/', views.login_admin, name='login_admin'),
    path('users/login_owner/', views.login_owner, name='login_owner'),
    path('users/logout_page/', views.logout_page, name='logout_page'),

]