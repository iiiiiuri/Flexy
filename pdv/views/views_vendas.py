from django.shortcuts import render
from pdv.models import Produto,Venda
from django.http import JsonResponse
from pdv.models import ProdutoVendido
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from pdv.models import Venda, Produto, ProdutoVendido, DescontosTroca
from datetime import date
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required
def renderizar_venda(request):
    return render(request, 'pdv/vendas.html')


def dicionario_vendas(request):
    vendas = Venda.objects.filter(empresa=request.user.empresa).order_by('data')
    vendas_list = []
    for venda in vendas:
        produtos_vendidos = ProdutoVendido.objects.filter(codigo_venda=venda.codigo, empresa=request.user.empresa)
        for produto_vendido in produtos_vendidos:
            metodos_de_pagamento = {}
            if venda.valor_pix > 0:
                metodos_de_pagamento['pix'] = venda.valor_pix
            if venda.valor_cartao > 0:
                metodos_de_pagamento['cartao'] = venda.valor_cartao
            if venda.valor_dinheiro > 0:
                metodos_de_pagamento['dinheiro'] = venda.valor_dinheiro
            if venda.valor_desconto > 0:
                metodos_de_pagamento['desconto'] = venda.valor_desconto

            venda_dict = {
                'codigo_venda': venda.codigo,
                'nome_produto': produto_vendido.produto.nome,
                'quantidade_comprada': produto_vendido.quantidade,
                'valor_unitario': '{:,.2f}'.format(produto_vendido.valor_unitario).replace(",", "x").replace(".", ",").replace("x", "."),
                'valor_total_item': '{:,.2f}'.format(produto_vendido.valor_total).replace(",", "x").replace(".", ",").replace("x", "."),
                'valor_total_venda': '{:,.2f}'.format(venda.valor_total).replace(",", "x").replace(".", ",").replace("x", "."), 
                'metodos_de_pagamento': metodos_de_pagamento,
                'troco': venda.troco,
                'vendedor': venda.vendedor,
                'data': venda.data.strftime('%d/%m/%Y'),
                'hora': venda.hora.strftime('%H:%M'),
                'status': produto_vendido.status
            }
            vendas_list.append(venda_dict)
    return vendas_list


def dadosVenda(request, id):
    venda = Venda.objects.get(codigo=id, empresa=request.user.empresa)
    produtos = ProdutoVendido.objects.filter(codigo_venda=id, empresa=request.user.empresa)
    total_quantidade = sum([produto.quantidade for produto in produtos])
    if total_quantidade <= 0:
        return JsonResponse({'error': 'A venda selecionada não tem produtos com quantidade maior que 0'})

    produtos_list = [produto.produto.nome for produto in produtos]
    produtos_codigo = [produto.produto.codigo for produto in produtos]
    produtos_quantidade = [produto.quantidade for produto in produtos]
    produtos_valor_unitario = [produto.valor_unitario for produto in produtos]

    produtosComCodigo = []
    for i in range(len(produtos_list)):
        produtosComCodigo.append({'nome': produtos_list[i],
                                  'codigo': produtos_codigo[i],
                                  'quantidade': produtos_quantidade[i],
                                  'valor_unitario': produtos_valor_unitario[i]})

    produtosDisponiveis_list = [produto.nome for produto in Produto.objects.filter(empresa=request.user.empresa)]
    produtosDisponiveis_codigo = [produto.codigo for produto in Produto.objects.all()]
    produtosDisponiveis_valor_unitario = [produto.preco for produto in Produto.objects.all()]

    produtosDisponiveis = []
    for i in range(len(produtosDisponiveis_list)):
        produtosDisponiveis.append({'nome': produtosDisponiveis_list[i],
                                    'codigo': produtosDisponiveis_codigo[i],
                                    'valor_unitario': produtosDisponiveis_valor_unitario[i]})

    return JsonResponse({
        'venda_selecionada': {
            'venda': venda.codigo,
            'produtos': produtosComCodigo,
            'valor_total': venda.valor_total,
            'troco': venda.troco,
            'vendedor': venda.vendedor,
        },
        'produtos_disponiveis': produtosDisponiveis
    })

@csrf_exempt
def efetuar_troca(request, id):
    if request.method == 'POST':
        data = json.loads(request.body)
        venda = Venda.objects.get(codigo=id, empresa=request.user.empresa)
        produtos = ProdutoVendido.objects.filter(codigo_venda=id, empresa=request.user.empresa)
        
        # Encontre o produto antigo e retorne a quantidade ao estoque
        produto_antigo = produtos.get(produto__codigo=data['produtos']['produtoAntigo'])
        valor_produto_antigo = produto_antigo.produto.preco * int(data['produtos']['qtdProdutoAntigo'])
        produto_antigo.produto.estoque += int(data['produtos']['qtdProdutoAntigo'])
        produto_antigo.status = 'Troca Realizada'
        produto_antigo.produto.save()
    
        # Se a quantidade do produto antigo for igual à quantidade devolvida, remova o produto antigo da venda
        if produto_antigo.quantidade == int(data['produtos']['qtdProdutoAntigo']):
            produto_antigo.quantidade = 0
            produto_antigo.save()
        else:
            # Caso contrário, subtraia a quantidade devolvida da quantidade do produto antigo na venda
            produto_antigo.quantidade -= int(data['produtos']['qtdProdutoAntigo'])
            produto_antigo.save()
    
        # Crie um novo Código de Troca
        codigo_troca = DescontosTroca.objects.all()
        valorCodigo = data['codigoGerado']['valor']

        valorCodigo = valorCodigo.replace(',', '.')
        valorCodigo = float(valorCodigo.replace('R$', ''))

        DescontosTroca.objects.create(
            valor_desconto=valorCodigo,
            data = date.today(),
            empresa = request.user.empresa,
            codigo_desconto = data['codigoGerado']['cod']
        )
    
        # Ajuste o valor total da venda
        venda.valor_total = round(venda.valor_total - valor_produto_antigo, 2)

        venda.status = 'Código de Troca Gerado'
        venda.save()
        return redirect('vendas')
    return JsonResponse({'message': 'Método não permitido'}, status=405)