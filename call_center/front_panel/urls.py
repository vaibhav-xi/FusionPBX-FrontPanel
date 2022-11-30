from django.contrib.auth.views import LogoutView
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('adminpanel/', views.AdminPanel, name="admin_panel"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('login/', views.Login, name="login"),
    path('register/', views.Register, name="register"),
    path('logout/', LogoutView.as_view(next_page="login"), name='logout'),
    path('make_call/', views.Make_Call, name="make_call"),

]

