from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_or_register, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('comp/<comp_code>/setup/', views.comp_setup, name='comp_setup'),
    path('comp/create/', views.comp_create, name='comp_create'),
    path('comp/<comp_code>/remove/', views.delete_question, name='delete_question'),
    path('comp/join/', views.comp_join, name='comp_join'),
    # Add other URL patterns as needed
]