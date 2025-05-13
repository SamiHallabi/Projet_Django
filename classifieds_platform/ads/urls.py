from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('ad/create/', views.ad_create, name='ad_create'),
    path('ad/<int:ad_id>/', views.ad_detail, name='ad_detail'),
    path('inbox/', views.inbox, name='inbox'),
    path('conversation/<int:user_id>/<int:ad_id>/', views.conversation, name='conversation'),
    path('conversation/<int:user_id>/', views.conversation, name='conversation'),
    path('profile/', views.profile, name='profile'),
]