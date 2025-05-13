from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('choose-interest/', views.choose_interest, name='choose_interest'),
    path('events/', views.events, name='view_events'),
    path('filtered_matches/', views.filtered_matches, name='filtered_matches'),
    path("accounts/verify/", views.verify_code, name="verify_code"),
    path('get_support/', views.get_support, name='get_support'),
]


