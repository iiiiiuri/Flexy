from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Sum, F
from pdv.models import Venda, ProdutoVendido
from django.db.models import Count
from django.db.models.functions import ExtractHour
from django.utils import timezone
from django.contrib.auth.decorators import login_required


@login_required
def analise(request):
    return render(request, 'pdv/analise.html')


def getMetodoPagamento(request):
    today = timezone.now().date()
    vendas_today = Venda.objects.filter(empresa=request.user.empresa, data__date=today)
    print(vendas_today)

    valor_pix = vendas_today.aggregate(Sum('valor_pix'))['valor_pix__sum'] or 0
    valor_cartao = vendas_today.aggregate(Sum('valor_cartao'))['valor_cartao__sum'] or 0
    valor_dinheiro = vendas_today.aggregate(Sum('valor_dinheiro'))['valor_dinheiro__sum'] or 0
    valor_codigo = vendas_today.aggregate(Sum('valor_desconto'))['valor_desconto__sum'] or 0

    verify = valor_pix + valor_cartao + valor_dinheiro + valor_codigo

    if verify == 0:
        return JsonResponse([], safe=False)
    else:
        return JsonResponse({'Pix': round(valor_pix,2),
                             'Cartão': round(valor_cartao,2),
                             'Dinheiro': round(valor_dinheiro,2),
                             'Código': round(valor_codigo,2)})

def getTopProdutosPerHour(request):
    today = timezone.now().date()
    produtoVendido = ProdutoVendido.objects.filter(
        produto__empresa=request.user.empresa, 
        status='Finalizada', 
        codigo_venda__in=Venda.objects.filter(data__date=today).values('codigo')
    ).values('produto__nome').annotate(quantidade=Sum('quantidade')).order_by('-quantidade')[:7]    
    produtos = []

    for produto in produtoVendido:
        produtos.append({
            'nome': produto['produto__nome'],
            'quantidade': produto['quantidade']
        })

    return JsonResponse({'produtos': produtos})
    
def getVendasPerHour(request):
    today = timezone.now().date()

    
    vendas = Venda.objects.filter(empresa=request.user.empresa, data__date=today).annotate(
        hora_extracted=ExtractHour('hora')
    ).values('hora_extracted').annotate(
        quantidade=Count('id'), 
        valor_total=Sum(F('valor_pix') + F('valor_dinheiro') + F('valor_cartao'))  # Soma os valores de valor_pix, valor_dinheiro e valor_cartao
    ).order_by('hora_extracted')

    print(vendas)
    vendas_list = []
    for venda in vendas:
        vendas_list.append({
            'hora': str(venda['hora_extracted']) + ':00',
            'quantidade': venda['quantidade'],
            'valor_total': venda['valor_total']  # Use 'valor_total' aqui
        })

    return JsonResponse({'vendas': vendas_list})

def getVendasPerVendedor(request):
    today = timezone.now().date()
    vendas = Venda.objects.filter(empresa=request.user.empresa, data__date=today).values('vendedor').annotate(
        quantidade=Count('id'), 
        valor_total=Sum(F('valor_pix') + F('valor_dinheiro') + F('valor_cartao'))  # Soma os valores e subtrai o desconto
    ).order_by('-valor_total')
    
    print(vendas)
    vendas_list = []
    for venda in vendas:
        vendas_list.append({
            'vendedor': venda['vendedor'],
            'quantidade': venda['quantidade'],
            'valor_total': round(venda['valor_total'],2)
        })

    return JsonResponse({'vendas': vendas_list})