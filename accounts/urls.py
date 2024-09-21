from django.urls import path,include
from . views import UserRegisterView, UserLogin,UserLogoutView, PasschangView, DepositMoneyView,update_profile 
urlpatterns = [
    path('register/',UserRegisterView.as_view(),name='register'),
    path('login/',UserLogin.as_view(),name='login'),
    path('logout/',UserLogoutView.as_view(),name='logout'),
    path('pass_change/', PasschangView.as_view(), name='pass_change'),
    path('deposite/', DepositMoneyView.as_view(),name='deposite'),
    path('profile/update/', update_profile, name='update_profile'),

]