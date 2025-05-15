from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('choose-interest/', views.choose_interest, name='choose_interest'),
    path('events/', views.events, name='view_events'),
    path('filtered_matches/', views.filtered_matches, name='filtered_matches'),
    path("accounts/verify/", views.verify_code, name="verify_code"),
    path('get_support/', views.get_support, name='get_support'),
    path('chat/<str:username>/', views.chat, name='chat'),
    path('chats/', views.chat_list, name='chat_list'),
    path('profile/', views.view_profile, name='view_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('user/<str:username>/', views.view_user_profile, name='view_user_profile'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]
