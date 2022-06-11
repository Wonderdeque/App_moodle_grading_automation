import django
from django.urls import path,include
from . import views

urlpatterns = [
     path('', include('django.contrib.auth.urls')),
     path('',views.index,name = 'home'),
     path('assigns',views.assigns,name="assigns"),
     path('antiplagiarism',views.plagiarism_answers,name="antiplagiarism"),
     path('screen_test',views.screen_test,name="screen_test")
]

