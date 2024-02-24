from django.urls import path
from . import views
from django.contrib.auth.views import LoginView,LogoutView
urlpatterns = [
     path('', views.index, name="home"),
     path('dashboard/', views.dashboard, name="dashboard"),
     path('login/', LoginView.as_view(), name="login_url"),
     path('register/', views.register, name="register_url"),
     path('logout/', LogoutView.as_view(), name="logout"),
]