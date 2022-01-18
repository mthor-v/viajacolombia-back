"""bookings_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView)
from booking_app.views.userView import UserCreateView, UserView
from booking_app.views.routeView import RouteView, ToUserView
from booking_app.views.ticketView import TicketView, ToCompanyView


urlpatterns = [
    path('login/', TokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('create/', UserCreateView.as_view()),
    path('user/', UserView.as_view()),
    path('user/del/<int:pk>/', UserView.as_view()),
    path('route/', RouteView.as_view()),
    path('route/del/<str:verif>/', RouteView.as_view()),
    path('route/user/<str:query>/', ToUserView.as_view()),
    path('ticket/', TicketView.as_view()),
    path('ticket/get-del/<str:verif>/', TicketView.as_view()),
    path('ticket/<str:idTrip>/', ToCompanyView.as_view())
]
