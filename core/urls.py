from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('registration/', views.registration, name='registration'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('profile/', views.profile, name='profile'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('carrito/', views.carrito, name='carrito'),
    path('adventure/', views.adventure, name='adventure'),
    path('racing/', views.racing, name='racing'),
    path('shooter/', views.shooter, name='shooter'),
    path('strategy/', views.strategy, name='strategy'),
    path('terror/', views.terror, name='terror'),
    path('registrar_usuario/', views.register_user, name='registrar_usuario'),
    path('user_login/', views.user_login, name='user_login'), 
    ]
