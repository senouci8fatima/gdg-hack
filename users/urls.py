from django.urls import path
from . import views

urlpatterns = [   
   
    path('sign_in', views.sign_in, name='sign_in'),
    path('sign_up', views.sign_up, name='sign_up'),
    path("demande/add/", views.add_demande, name="add_demande"),
    path("demandes/", views.list_demandes, name="list_demandes"),
    path("demande/<int:demande_id>/response/", views.create_response, name="create_response"),
    path("demande/<int:demande_id>/responses/", views.list_responses, name="list_responses"),
    path("demande/add-page/", views.add_demande_page, name="add_demande_page"),
    path("demandes/page/", views.list_demandes_page, name="list_demandes_page"),
    path('HomePage', views.HomePage, name='HomePage'),
    path('help', views.help, name='help'),
    path('askHelp/', views.askHelp, name='ask_help'),  # Define URL name
    path('', views.home, name='home'),  # Define URL name
    path("classement/", views.Classement, name="classement"),
    path("rewards/", views.Rewards, name="rewards"),
    path('challenges/', views.challenges, name='challenges'),
    path("add-question/", views.add_question, name="add_question"),
    path("add-coins/", views.add_coins, name="add_coins"),
    path("create-meet", views.create_meet, name="create_meet"),
    path("CoursesPage", views.CoursesPage, name="CoursesPage"),
    path('courses/<str:category>/', views.filter_courses, name='filter_courses'),
    path("join-course/<int:course_id>/", views.join_course, name="join_course"),
    path("rate_course/<int:course_id>/", views.rate_course, name="rate_course"),
    path("add-to-agenda/<int:course_id>/", views.add_to_agenda, name="add_to_agenda"),
]