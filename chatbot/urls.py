from chatbot import views
from django.urls import path


urlpatterns = [
    path('',views.home,name='home'),
    path('register/',views.user_register,name='register'),
    path('login/', views.user_login, name='login'),
    path('chabot/',views.chatbot,name='chatbot'),
    path('logout/', views.user_logout, name='logout'),

]