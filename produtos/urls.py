from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('produto/<int:pk>/', views.product_detail, name='product_detail'),  # Ajustado para usar pk
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/', views.profile, name='profile'),
    path('editar_perfil/', views.edit_profile_view, name='edit_profile'),
    path('registrar_produto/', views.registrar_produto, name='registrar_produto'),
    path('registrar_avaliacao/<int:produto_id>/', views.registrar_avaliacao, name='registrar_avaliacao'),
    path('produto_detalhe/<int:produto_id>/', views.produto_detalhe, name='produto_detalhe'),  # Renomeado para evitar conflito
    path('apagar_avaliacao/<int:avaliacao_id>/', views.apagar_avaliacao, name='apagar_avaliacao'),
]
