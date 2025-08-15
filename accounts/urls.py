from django.contrib.auth import views
from django.urls import path
from accounts import views



urlpatterns = [
    
  path('',views.ks_login,name="login"),
  path('register',views.register,name="register"),
  path('newuser',views.create_user,name="newuser"),
  path('updateuser',views.updateuser,name="updateuser"),
  path('reset_pass',views.reset_pass,name="reset_pass"),
  path('reset_pass_username',views.reset_pass_username,name="reset_pass_username"),


  path('password_reset', views.passwword_reset, name= "passwordreset"),
  path('logout/', views.logout_request, name= "logout"), 
  
  
]
