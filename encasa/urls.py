from django.contrib import admin
from django.urls import path
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf.urls.static import static
from django.views.static import serve

from django.conf import settings
urlpatterns = [
	path('', include('core.urls')),
	path('orcamento/', include('orcamento.urls')),
	path('placas/', include('placas.urls')),
    path('imagens/<path>', serve, {
		'document_root': settings.MEDIA_ROOT,
	}),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Servir arquivos de mídia localmente