from django.urls import path
from . import views


urlpatterns = [
    # path("<str:user>/", views.Home, name="home"),
    path("", views.Home, name="home"),
    path("register/forum", views.RegisterUserPage, name="registerforum"),
    path("register", views.RegisterUser, name="registeruser"),   
    path("login/forum", views.LoginUserPage, name="loginforum"), 
    path("login", views.LoginUser, name="loginuser"),
    # path("logout", views.LogoutUser, name="logoutuser"),

    path("admin", views.AdminDashboard, name="admindashboard"),
    path("register/admin/forum", views.RegisterAdminPage, name="registeradminforum"),
    path("register/admin", views.RegisterAdmin, name="registeradmin"),
    path("login/admin/forum", views.LoginAdminPage, name="loginadminforum"),
    path("login/admin", views.LoginAdmin, name="loginadmin"),

    path("getbyid/<str:id>/", views.GetIdUser, name="gettinbyid"),
    path("update/<str:id>/", views.UpdateUser, name="updateuser"),
    path("delete/<str:id>/", views.DeleteUser, name="deleteuser"),
]