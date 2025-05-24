from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout', kwargs={'template_name': 'logout.html'}),
    path('ad/create/', views.ad_create, name='ad_create'),
    path('ad/<int:ad_id>/', views.ad_detail, name='ad_detail'),
    path('inbox/', views.inbox, name='inbox'),
    path('conversation/<int:user_id>/', views.conversation, name='conversation'),
    path('conversation/<int:user_id>/<int:ad_id>/', views.conversation, name='conversation'),
    path('profile/', views.profile, name='profile'),
    path('ad/<int:ad_id>/report/', views.report_ad, name='report_ad'),
    path('report_management/', views.report_management, name='report_management'),
    
   
   
]