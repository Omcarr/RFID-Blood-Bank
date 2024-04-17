from django.urls import path
from . import views


urlpatterns =[
    path('', views.home,name='home'),
    path('login/', views.loginPage,name='login'),
    path('logout/', views.logoutUser, name="logout"),
     path('register/<int:group_id>/', views.register, name="register"),
    path('Admin_register/', views.Admin_register, name="Admin_register"),
    path('CreateDrive/', views.CreateDrive, name="CreateDrive"),

]
