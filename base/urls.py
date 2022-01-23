from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('room/<str:pk>/', views.room, name = 'room'),
    path('create_room/', views.create_room, name = 'create_room'),
    path('update_room/<str:pk>/', views.update_room, name = 'update_room'),
    path('delete_room/<str:pk>/', views.delete_room, name = 'delete_room'),
    path('login/', views.loginUser, name = 'login'),
    path('logout/', views.logoutUser, name = 'logout'),
    path('register/', views.registerUser, name = 'register'),
    path('delete_message/<str:pk>/', views.deleteMessage, name = 'delete_message'),
    path('user_profile/<str:pk>/', views.userProfile, name = 'user_profile'),
    path('edit_user/', views.editUser, name = 'edit_user'),
    path('topics/', views.topicsView, name = 'topics'),
    path('activities/', views.activities, name = 'activities')
]