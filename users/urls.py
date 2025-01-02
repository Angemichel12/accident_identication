from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_view, name='logout'),
    path('users/add/', views.register_user_view, name='register_user'),
    path('users/edit/', views.edit_user, name='edit_user'),
    path('users/delete/<int:user_id>/', views.delete_user_view, name='delete_user'),
]
