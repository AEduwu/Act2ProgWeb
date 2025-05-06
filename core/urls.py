from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import GameListAPIView, UserListAPIView

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
    path('carrito/', views.carrito, name='carrito'),
    path('carrito/add/<int:cod_game>/', views.cart_add, name='cart_add'),
    path('carrito/down/<int:cod_game>/', views.cart_down, name='cart_down'),
    path('carrito/remove/<int:cod_game>/', views.cart_remove, name='cart_remove'),
    path('gameAdministration/', views.gameAdministration, name='gameAdministration'),
    path('admin/juegos/', views.gameAdministration, name='game_admin'),
    path('juegos/', views.create_game, name='create_game'),
    path('juegos/update/<int:cod_game>/', views.update_game, name='update_game'),
    path('juegos/delete/<int:cod_game>/', views.delete_game, name='delete_game'),
    path('recuperar/', views.recuperar_clave, name='recuperar_clave'),
    path('restablecer/<uidb64>/', views.restablecer, name='restablecer'),
    path('editar-perfil/', views.editar_perfil, name='editar_perfil'),
    path('api/games/', GameListAPIView.as_view(), name='api-games'),
    path('api/users/', UserListAPIView.as_view(), name='api-users'),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)