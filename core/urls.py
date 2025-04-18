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
    path('close_session/', views.close_session, name='close_session'), 
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:cod_game>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:cod_game>/', views.cart_remove, name='cart_remove'),
    path('gameAdministration/', views.gameAdministration, name='gameAdministration'),
    path('admin/juegos/', views.gameAdministration, name='game_admin'),
    path('admin/juegos/create/', views.create_game, name='create_game'),
    path('admin/juegos/update/<int:cod_game>/', views.update_game, name='update_game'),
    path('admin/juegos/delete/<int:cod_game>/', views.delete_game, name='delete_game'),
    ]
