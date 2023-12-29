from django.urls import path
from . import views

urlpatterns = [
	path('login/', views.login, name='login'),
	path('create_user/', views.create_user, name='create_user'),
	path('get_all_users/', views.get_all_users, name='get_all_users'),
	path('excluir_user/', views.excluir_user, name='excluir_user'),
	path('verifica_token/', views.verifica_token, name='verifica_token'),
	path('renova_token/', views.renova_token, name='renova_token'),
]