from django.shortcuts import render, redirect
from pdv.models import Produto
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required

@login_required
def editar(request):

    if not request.user.proprietario:
        return redirect('pagamento')

    categorias = [choice[0] for choice in Produto.CATEGORIA_CHOICES]
    subcategorias = [choice[0] for choice in Produto.SUB_CHOICES]
    tamanhos = [choice[0] for choice in Produto.TAMANHO_CHOICES]
    produtos = Produto.objects.all()
    
    return render(request, 'pdv/editar.html', {
        'produtos': produtos,
        'user': request.user,
        'categorias' : categorias,
        'subcategorias' : subcategorias,
        'tamanhos' : tamanhos
        })
    
def itemEditar(request, id):

    if not request.user.proprietario:
        return redirect('pagamento')

    produtos = Produto.objects.all()

    if request.method == 'POST':
        codigo = request.POST.get('codigo')
        nome = request.POST.get('nome')
        cor = request.POST.get('cor')
        categoria = request.POST.get('categoria')
        subcategoria = request.POST.get('subcategoria')
        preco = request.POST.get('preco')
        tamanho = request.POST.get('tamanho')
        estoque = request.POST.get('estoque')

        try:
            produto = Produto.objects.get(id=id)
            if codigo:
                produto.codigo = codigo
            if nome:
                produto.nome = nome
            if cor:
                produto.cor = cor
            if categoria:
                produto.categoria = categoria
            if subcategoria:
                produto.subcategoria = subcategoria
            if preco:
                produto.preco = preco
            if tamanho:
                produto.tamanho = tamanho
            if estoque:
                produto.estoque = estoque
            produto.save()
            return redirect('editar')
        except Exception as e:
            return render(request, 'pdv/editar.html', {'error': 'Erro ao alterar produto', 'produtos': produtos})
    else:
        

        return render(request, 'pdv/editar.html', {
            'produtos': produtos,

            })

def itemSelecionado(request, id):
    produto = Produto.objects.get(id=id)
    return JsonResponse({'produtoSelecionado': model_to_dict(produto)})