from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.decorators import api_view, permission_classes
import json
from django.core import serializers
from rest_framework.permissions import IsAuthenticated
from .models import Orcamento, Irradiacao

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def salvar(request):
    corpo = json.loads(request.body)
    print(corpo['cmtotal'])
    entrega = Orcamento(
        nome = corpo['nome'],
        cep = corpo['cep'],
        rua = corpo['rua'],
        cidade = corpo['cidade'],
        bairro = corpo['bairro'],
        numero = corpo['numero'],
        total = corpo['total'],
        avista = corpo['avista'],
        entrada = corpo['entrada'],
        qtdx = corpo['qtdx'],
        p12 = corpo['p12'],
        p24 = corpo['p24'],
        p36 = corpo['p36'],
        p48 = corpo['p48'],
        p60 = corpo['p60'],
        modulos = corpo['modulos'],
        mmarca = corpo['mmarca'],
        inversor = corpo['inversor'],
        imarca = corpo['imarca'],
        conectores = corpo['conectores'],
        select = corpo['select'],
        preto = corpo['preto'],
        vermelho = corpo['vermelho'],
        garantia_modulos = corpo['garantia_modulos'],
        garantia_inversor = corpo['garantia_inversor'],
        garantia_estrutura = corpo['garantia_estrutura'],
        garantia_demais = corpo['garantia_demais'],
        garantia_por = corpo['garantia_por'],
        garantia_anos = corpo['garantia_anos'],
        consumo = corpo['consumo'],
        entrada_fin = corpo['entrada_fin'],
        valor_fin = corpo['valor_fin'],
        id_modulo = corpo['id_modulo'],
        cmtotal = corpo['cmtotal'],
    )
    
    entrega.save()
    id_salvo = entrega.id

    irradiacao = Irradiacao(
        ID_IR = entrega.id,
        ANNUAL=corpo['ANNUAL'],
        JAN=corpo['JAN'],
        FEB=corpo['FEB'],
        MAR=corpo['MAR'],
        APR=corpo['APR'],
        MAY=corpo['MAY'],
        JUN=corpo['JUN'],
        JUL=corpo['JUL'],
        AUG=corpo['AUG'],
        SEP=corpo['SEP'],
        OCT=corpo['OCT'],
        NOV=corpo['NOV'],
        DEC=corpo['DEC'],
    )
    irradiacao.save()
    return JsonResponse({'status': '200', 'id_salvo': id_salvo}, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def getOrcamento(request):
    print(request)
    corpo = json.loads(request.body)
    print(corpo)
    id = corpo['id']
    orcamento = Orcamento.objects.filter(id=id)
    print(orcamento)
    if not orcamento.exists():
        return JsonResponse({'message': 'Orçamento não encontrado'}, status=410)

    irradiacao = Irradiacao.objects.filter(ID_IR = id)
    print(irradiacao)
    orcamento_ = json.loads(serializers.serialize('json', orcamento))
    irradiacao_ = json.loads(serializers.serialize('json', irradiacao))
    print(irradiacao_)
    return JsonResponse({'orcamento': orcamento_,'irradiacao': irradiacao_ }, status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def getNomeOrcamento(request):
    corpo = json.loads(request.body)
    nome = corpo['nome']
    orcamento = Orcamento.objects.filter(nome__icontains=nome).values('id', 'nome', 'data')
    orcamento_list = list(orcamento)
    
    if not orcamento_list:
        return JsonResponse({'message': 'Orçamento não encontrado'}, status=410)

    return JsonResponse({'orcamento': orcamento_list}, status=200, safe=False)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def getListaOrcamento(request):
    orcamento = Orcamento.objects.all().order_by("-id").values('id', 'nome', 'data')

    return JsonResponse({'orcamento': list(orcamento)}, status=200)
