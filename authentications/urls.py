"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from authentications import views
from .views import SignupApiView,LoginAPIView,managerAPIView,ConsumerAPIView,add_inventryAPIView,view_inventryAPIView ,view_inventry, update_inventryAPIView,delete_inventryAPIView,orderAPIView, profileAPIView, cartpageAPIView, manager_page,  delete_page, update_inventry
urlpatterns = [
    path('', 
            SignupApiView.as_view(),
            name="signup"),
    path('login/', 
         LoginAPIView.as_view(),
         name="login"), 

    path('manager_api/', 
             managerAPIView.as_view(),
             name="manager_api"),
    path("manager_deshboard/", manager_page, name="manager"),  
    path('consumerdeshboard/', 
                 ConsumerAPIView.as_view(),
                 name="consumer"),
    path('Cart/',cartpageAPIView.as_view(),
                         name="cartpage"),
                
    path('orders/',orderAPIView.as_view(),
                         name="order"),
    path('profile/',profileAPIView.as_view(),
                             name="profile"),
                             
    path('add_inventry/',
         add_inventryAPIView.as_view(),
         name="add_inventry"),

    path("view_inventry_api/",
         view_inventryAPIView.as_view(),
         name="view_inventry_api"),
    path("view_inventry/",
             view_inventry,
             name="view_inventry"),
    path("update_inventry_api/"
         ,update_inventryAPIView.as_view(),
         name="update_inventry_api"),
    path("update_inventry/",
         update_inventry,name="update_inventry"),
    path("delete_inventry_api/"
             ,delete_inventryAPIView.as_view(),
             name="delete_inventry_api"),
    path("delete_inventry/",
         delete_page,name="delete_inventry")
    
]