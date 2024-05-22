from django.shortcuts import render
from pdv.models import Produto, User, DescontosTroca
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.decorators import login_required

@login_required
def pagamento(request):
    produtos = Produto.objects.filter(empresa=request.user.empresa)
    for produto in produtos:
        produto.preco = "{:.2f}".format(produto.preco)
    vendedores = User.objects.filter(vendedor=True, empresa=request.user.empresa)

    context = {
        'produtos': produtos,
        'vendedores': vendedores,
        'user': request.user
    }

    return render(request, 'pdv/pagamento.html', context)


def resumoCompra(request, cod):
    produto = Produto.objects.get(codigo=cod, empresa=request.user.empresa)

    compra = {
        'codigo': produto.codigo,
        'nome': produto.nome,
        'preco': produto.preco,
        'estoque' : produto.estoque
    }

    # Adicione o produto ao resumo de compra na sessão
    if 'resumo_compra' not in request.session:
        request.session['resumo_compra'] = []
    
    for item in request.session['resumo_compra']:
        if item['codigo'] == cod:
            item['quantidade'] += 1
            break
    else:
        compra['quantidade'] = 1
        request.session['resumo_compra'].append(compra)

    request.session.modified = True

    return JsonResponse({'compra': compra})



def removeCompra(request, cod):
    # Remova o produto do resumo de compra na sessão
    if 'resumo_compra' in request.session:
        for item in request.session['resumo_compra']:
            if item['codigo'] == cod:
                item['quantidade'] -= 1
                if item['quantidade'] <= 0:
                    request.session['resumo_compra'].remove(item)
                break

        request.session.modified = True

    return JsonResponse({'success': True})



@csrf_exempt
def codVerify(request,cod):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            desconto = DescontosTroca.objects.get(codigo_desconto=data['codigo'])
            return JsonResponse({'existe': True, 'valor_desconto': desconto.valor_desconto})
        except DescontosTroca.DoesNotExist:
            return JsonResponse({'existe': False})



def dadosEmpresa(request, user):
    empresa = User.objects.get(username=user).empresa
    return JsonResponse({
        'nome': empresa.nome,
        'cnpj': empresa.cnpj,
        'endereco': empresa.endereco,
        'numero': empresa.numero,
        'telefone': empresa.telefone,
        'bairro': empresa.bairro,
        'email': empresa.email,
        'cep': empresa.cep
    })