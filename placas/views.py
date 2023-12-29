
import os
import uuid
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile
from django.forms import ValidationError

from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
import json
from django.core import serializers
from rest_framework.permissions import IsAuthenticated
from .models import Placas, SolarData
import pandas as pd
from django.db import transaction

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def salvar(request):
    corpo = request.POST  # Acessar os dados do formulário enviado

    # Certifique-se de que 'img' corresponde ao nome do campo no FormData
    imagem = request.FILES.get('img')  # Use request.FILES para acessar arquivos enviados

    if imagem:
        try:
            # Salvar a imagem com um nome único no diretório 'placas'
            image_name = f'imagens/{str(uuid.uuid4())}.png'
            image_path = os.path.join(settings.MEDIA_ROOT, image_name)

            with open(image_path, 'wb') as image_file:
                for chunk in imagem.chunks():
                    image_file.write(chunk)

            # Crie um objeto Placas com os dados recebidos
            placa = Placas(
                marca=corpo.get('marca'),
                modelo=corpo.get('modelo'),
                watts=corpo.get('watts'),
                eficiencia=corpo.get('eficiencia'),
                largura=corpo.get('largura'),
                altura=corpo.get('altura'),
                img=image_name,  # Use o nome do arquivo salvo
            )

            placa.save()

            return JsonResponse({'status': 200})
        except Exception as e:
            return JsonResponse({'status': 500, 'error': str(e)})
    else:
        return JsonResponse({'status': 400, 'message': 'Imagem não encontrada no FormData'})
@api_view(['POST'])
@permission_classes([IsAuthenticated])

def alterar(request):
    imagem = request.FILES.get('img')  # Use request.FILES para acessar arquivos enviados

    if imagem:
        # Salvar a imagem com um nome único no diretório 'placas'
        image_name = f'imagens/{str(uuid.uuid4())}.png'
        image_path = os.path.join(settings.MEDIA_ROOT, image_name)

        with open(image_path, 'wb') as image_file:
            for chunk in imagem.chunks():
                image_file.write(chunk)

    corpo = json.loads(request.body)
    id = corpo['id']
    marca = corpo['marca']
    modelo = corpo['modelo']
    watts = corpo['watts']
    eficiencia = corpo['eficiencia']
    largura = corpo['largura']
    altura = corpo['altura']

    placa = get_object_or_404(Placas, id=id)
    
    try:
        placa.marca = marca
        placa.modelo = modelo
        placa.watts = watts
        placa.eficiencia = eficiencia
        placa.largura = largura
        placa.altura = altura
        placa.img = image_name

        placa.save()

        return JsonResponse({'status':'200'})
    except:
        return JsonResponse({'status': '500'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def excluir(request):
    corpo = json.loads(request.body)
    id = corpo['id']
    
    print(id)
    user = get_object_or_404(Placas, id=id)
    user.delete()

    return JsonResponse({'status': '200', 'message': 'Usuário excluído com sucesso'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def getPlaca(request):
    corpo = json.loads(request.body)
    id = corpo['id']
    placa = Placas.objects.filter(id=id).first()

    placa_list = json.loads(serializers.serialize('json', placa))
    print(placa_list)
    if not placa_list:
        return JsonResponse({'message': 'Orçamento não encontrado'}, status=410)

    return JsonResponse({'placa': placa_list}, status=200, safe=False)


@api_view(['GET'])  # Altere para GET, pois estamos buscando dados
@permission_classes([IsAuthenticated])
def getAllPlaca(request):
    placas = Placas.objects.all()
    placa_list = json.loads(serializers.serialize('json', placas))
    return JsonResponse({'placas': placa_list}, status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def salvar_excel(request):
    if 'file' not in request.FILES:
        return JsonResponse({'error': 'Nenhum arquivo enviado'})

    excel_file = request.FILES['file']

    try:
        SolarData.objects.all().delete()
        df = pd.read_excel(excel_file)

        for index, row in df.iterrows():
            try:
                # Crie uma instância do modelo SolarData diretamente do DataFrame
                solar_data = SolarData(
                    LON=row['LON'],
                    LAT=row['LAT'],
                    NAME=row['NAME'],
                    CLASS=row['CLASS'],
                    STATE=row['STATE'],
                    ANNUAL=row['ANNUAL'],
                    JAN=row['JAN'],
                    FEB=row['FEB'],
                    MAR=row['MAR'],
                    APR=row['APR'],
                    MAY=row['MAY'],
                    JUN=row['JUN'],
                    JUL=row['JUL'],
                    AUG=row['AUG'],
                    SEP=row['SEP'],
                    OCT=row['OCT'],
                    NOV=row['NOV'],
                    DEC=row['DEC']
                )
                solar_data.full_clean()  # Valide os campos do modelo
                solar_data.save()
            except ValidationError as e:
                return JsonResponse({'error': 'Erro de validação: ' + str(e)})

        return JsonResponse({'success': 'Dados do arquivo Excel foram processados e salvos com sucesso'})
    except Exception as e:
        return JsonResponse({'error': 'Erro ao processar o arquivo Excel: ' + str(e)})
        


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def getIrradiacao(request):

    corpo = json.loads(request.body)
    cidade = corpo['cidade']
    print(cidade)
    irradiacao = SolarData.objects.filter(NAME=cidade)
    irradiacao_ = json.loads(serializers.serialize('json', irradiacao))
    if not irradiacao_:
        return JsonResponse({'message': 'Irradiação não encontrada'}, status=410)

    return JsonResponse({'irradiacao': irradiacao_}, status=200)
