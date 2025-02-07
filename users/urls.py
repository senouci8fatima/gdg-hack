from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.LandingPage, name='LandingPage'),
    path('HomePage', views.HomePage, name='HomePage'),
    path('sign_in', views.sign_in, name='sign_in'),
    path('sign_up', views.sign_up, name='sign_up'),



]