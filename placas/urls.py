from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
	path('salvar/', views.salvar, name='salvar'),
	path('alterar/', views.alterar, name='alterar'),
	path('excluir/', views.excluir, name='excluir'),
	path('getAllPlaca/', views.getAllPlaca, name='getAllPlaca'),
	path('salvar_excel/', views.salvar_excel, name='salvar_excel'),
	path('getIrradiacao/', views.getIrradiacao, name='getIrradiacao'),
    path('imagens/<path>', serve, {
		'document_root': settings.MEDIA_ROOT,
	}),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Servir arquivos de mídia localmente