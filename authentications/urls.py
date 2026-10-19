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
from .views import UserSignupApiView, ConsumerSignupApiView,LoginAPIView,managerAPIView,ConsumerAPIView,add_inventryAPIView,view_inventryAPIView,update_inventryAPIView,delete_inventryAPIView, Add_CartAPIView, orderAPIView, profileAPIView, cartpageAPIView
urlpatterns = [
    path('', 
        UserSignupApiView.as_view(),
        name="user_signup"),
    path('consumer/', 
            ConsumerSignupApiView.as_view(),
            name="consumer_signup"),

    path('login/', 
         LoginAPIView.as_view(),
         name="login"), 

    path('manager/', 
             managerAPIView.as_view(),
             name="manager"),
    path('consumerdeshboard/', 
                 ConsumerAPIView.as_view(),
                 name="consumer"),
    path('Cart/',cartpageAPIView.as_view(),
                         name="cartpage"),
    path('AddCart/',Add_CartAPIView.as_view(),
                     name="cart"),
    path('orders/',orderAPIView.as_view(),
                         name="order"),
    path('profile/',profileAPIView.as_view(),
                             name="profile"),
                             

    # path('supervisor/', 
    #                  supervisorAPIView.as_view(),
    #                  name="supervisor"),
    path('add_inventry/',
         add_inventryAPIView.as_view(),
         name="add_inventry"),

    path("view_inventry/",
         view_inventryAPIView.as_view(),
         name="view_inventry"),
    path("update_inventry/"
         ,update_inventryAPIView.as_view(),
         name="update_inventry"),
    path("delete_inventry/"
             ,delete_inventryAPIView.as_view(),
             name="delete_inventry")
    
]