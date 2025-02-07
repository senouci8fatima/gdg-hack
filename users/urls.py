from django.urls import path
from . import views

urlpatterns = [   
    path('', views.LandingPage, name='LandingPage'),
    path('sign_in', views.sign_in, name='sign_in'),
    path('sign_up', views.sign_up, name='sign_up'),
    path("demande/add/", views.add_demande, name="add_demande"),
    path("demandes/", views.list_demandes, name="list_demandes"),
    path("demande/<int:demande_id>/response/", views.create_response, name="create_response"),
    path("demande/<int:demande_id>/responses/", views.list_responses, name="list_responses"),
    path("demande/add-page/", views.add_demande_page, name="add_demande_page"),
    path("demandes/page/", views.list_demandes_page, name="list_demandes_page"),
    path('HomePage', views.HomePage, name='HomePage'),

]