from django.shortcuts import render, redirect
from pdv.models import Produto
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required

@login_required
def excluir(request):

    if not request.user.proprietario:
            return redirect('pagamento')

    produtos = Produto.objects.filter(empresa=request.user.empresa)
    return render(request, 'pdv/excluir.html', {'produtos': produtos})


def itemExcluir(request, id):

    if not request.user.proprietario:
            return redirect('pagamento')

    produtos = Produto.objects.filter(empresa=request.user.empresa)

    if Produto.objects.filter(id=id, empresa=request.user.empresa).exists():
        produto = Produto.objects.get(id=id, empresa=request.user.empresa)
        produto.delete()
        return render(request, 'pdv/excluir.html', {'success': 'Produto excluído com sucesso', 'produtos': produtos})
    else:
        return render(request, 'pdv/excluir.html', {'error': 'Produto não encontrado', 'produtos': produtos}) 