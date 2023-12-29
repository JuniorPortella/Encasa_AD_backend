from django.urls import path
from . import views

urlpatterns = [
	path('salvar/', views.salvar, name='salvar'),
	path('getOrcamento/', views.getOrcamento, name='getOrcamento'),
	path('getListaOrcamento/', views.getListaOrcamento, name='getListaOcamento'),
	path('getNomeOrcamento/', views.getNomeOrcamento, name='getNomeOrcamento'),
]