from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('crop/', views.crop_page),
    path('disease/', views.disease_page),
    path('history/',views.history_page,name='history'),
    path('guidance/', views.guidance_page, name='guidance'),

]