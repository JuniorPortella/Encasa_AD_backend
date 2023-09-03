from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model
from django.utils import timezone
import json
from django.shortcuts import get_object_or_404

import jwt
from django.conf import settings
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
User = get_user_model()


@permission_classes([])
def login(request):
    corpo = json.loads(request.body)
    username = corpo['username']
    password = corpo['password']
    
    user = authenticate(username=username, password=password)
    if user:
        access_token = AccessToken.for_user(user)
        
        # Gere um token de atualização
        refresh = RefreshToken.for_user(user)
        
        # Retorne os tokens na resposta
        return JsonResponse({
            'status': '200',
            'result': {
                'access_token': str(access_token),
                'refresh_token': str(refresh),
            }
        })
    else:
        return JsonResponse({'detail': 'Credenciais inválidas'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_user(request):
    corpo = json.loads(request.body)
    print(corpo, "teste")
    nome = corpo['nome']
    login = corpo['login']
    senha = corpo['senha']
    adm = corpo['adm']
    if request.user.username == login:
        return JsonResponse({'status': 'Você não pode alterar seu próprio perfil'}, status=301)
    
    existing_user = User.objects.filter(username=login).first()

    if existing_user:
        existing_user.set_password(senha)  # Atualize a senha
        existing_user.is_staff = adm  # Atualize a propriedade 'is_staff' para determinar se o usuário é um administrador
        existing_user.save()
        return JsonResponse({'status': '210'})
    else:
        user = User.objects.create_user(username=login, password=senha, first_name=nome, is_staff=adm )
        user.save()
        return JsonResponse({'status' : '200'}, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_all_users(request):
    # Busque todos os usuários no banco de dados
    users = User.objects.all()
    
    # Crie uma lista de dicionários com informações sobre cada usuário
    user_list = [
        {
            'id': user.id,
            'nome': user.first_name,
            'login': user.username,
            # Adicione outros campos conforme necessário
        }
        for user in users
    ]
    
    return JsonResponse(user_list, safe=False)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def excluir_user(request):
    # Verifique se o usuário com o ID fornecido existe
    
    corpo = json.loads(request.body)
    print(corpo, "teste")
    id = corpo['user_id']
    user = get_object_or_404(User, id=id)
    # Você pode adicionar verificações adicionais, como verificar se o usuário tem permissão para excluir
    # Realize a exclusão do usuário
    user.delete()

    # Responda com um JSON indicando sucesso
    return JsonResponse({'status': '200', 'message': 'Usuário excluído com sucesso'})
