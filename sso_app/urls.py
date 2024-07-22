from django.urls import path

from sso_app import views

urlpatterns = [
    path('login/', views.login_view, name='custom_login'),
    path('register/', views.register_view, name='custom_register'),
    path('logout/', views.logout_view, name='custom_logout'),
    path('profile/', views.update_profile, name='profile'),

]
