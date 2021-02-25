from django.urls import path
from . import views
urlpatterns =[
    path("",views.index,name="index"),path("login",views.login,name="login"),path("register",views.register,name="reg"),path("main",views.index,name="main"),
    path("entry",views.entry,name="entry"),path("logout",views.logout,name="lout"),path("display",views.display,name="display")
]