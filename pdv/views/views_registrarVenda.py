from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pdv.models import Venda, Produto, ProdutoVendido, DescontosTroca
import json

@csrf_exempt
def registrar_venda(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        # Obter o vendedor e os valores de pagamento
        vendedor = data.get('vendedor')
        valor_pix = data.get('valor_pix')
        valor_cartao = data.get('valor_cartao')
        valor_dinheiro = data.get('valor_dinheiro')
        valor_desconto = data['descontos']['valor_desconto']
        valor_sobra = data['descontos']['valor_extorno']
        troco = data.get('troco') if data.get('troco') else 0

        # Inicializar o valor total
        valor_total = 0

        # Iterar sobre os itens da venda
        for item in data['itens']:
            # Obter o produto
            produto = Produto.objects.get(codigo=item.get('cod'), empresa=request.user.empresa)

            # Atualizar o estoque do produto
            produto.estoque -= item.get('quantidade')
            produto.save()

            # Adicionar o valor do item ao valor total
            valor_total += float(item.get('valor')) * item.get('quantidade')

        # Criar a venda
        venda = Venda(
            codigo=Venda.objects.latest('codigo').codigo + 1 if Venda.objects.exists() else 1,
            valor_total=round(valor_total,2),
            vendedor=vendedor,
            valor_pix=valor_pix,
            valor_cartao=valor_cartao,
            valor_dinheiro=valor_dinheiro,
            valor_desconto=valor_desconto,
            troco=troco,
            empresa = request.user.empresa
        )
        
        venda.save()

        # Iterar sobre os itens da venda novamente para criar os ProdutosVendidos
        for item in data['itens']:
            
            produto = Produto.objects.get(codigo=item.get('cod'), empresa=request.user.empresa)
            # Criar o ProdutoVendido
            produto_vendido = ProdutoVendido(
                codigo_venda=venda.codigo,
                produto=produto,
                valor_unitario=float(item.get('valor')),
                quantidade=item.get('quantidade'),
                valor_total=float(item.get('valor')) * item.get('quantidade'),
                empresa = request.user.empresa,
                status='Finalizada',
                
            )
            produto_vendido.save()

            if data['descontos']['cod_desconto'].strip() != '':
                desconto = DescontosTroca.objects.get(codigo_desconto=data['descontos']['cod_desconto'])
                if valor_sobra != '':
                    desconto.valor_desconto = float(valor_sobra)  # Convert the string to a float before assigning it
                else:
                    desconto.valor_desconto = 0.0  # Use a default value if valor_sobra is an empty string
                desconto.save()


            
        return JsonResponse({'message': 'Venda registrada com sucesso!', 'redirect': '/pagamento'}, status=201)

    else:
        return JsonResponse({'error': 'Método inválido'}, status=400)