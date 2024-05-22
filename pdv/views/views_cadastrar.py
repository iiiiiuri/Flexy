from django.shortcuts import render, redirect
from pdv.models import Produto
from django.http import JsonResponse, HttpResponse
import csv
from django.contrib.auth.decorators import login_required

@login_required
def cadastrar(request):

    if not request.user.proprietario:
            return redirect('pagamento')

    ultimo_codigo = Produto.objects.latest('codigo').codigo if Produto.objects.exists() else None
    if request.method == 'POST':
        codigo = request.POST['codigo']
        nome = request.POST['nome']
        cor = request.POST['cor']
        categoria = request.POST['categoria']
        subcategoria = request.POST['subcategoria']
        preco = request.POST['preco']
        tamanho = request.POST['tamanho']
        estoque = request.POST['estoque']
        
        if Produto.objects.filter(codigo=codigo, empresa=request.user.empresa).exists():
            return render(request, 'pdv/cadastrar.html', {'error': 'Um produto com este código já existe'})

        try:
            produto = Produto.objects.create(
                codigo=codigo,
                nome=nome,
                cor=cor,
                categoria=categoria, 
                subcategoria=subcategoria,
                preco=preco,
                tamanho=tamanho, 
                estoque=estoque,
                empresa= request.user.empresa
                )
            
            produto.save()
            return render(request, 'pdv/cadastrar.html', {'success': 'Produto cadastrado com sucesso', 'ultimo_codigo': ultimo_codigo})
        except Exception as e:
            return render(request, 'pdv/cadastrar.html', {'error': 'Erro ao cadastrar produto', 'ultimo_codigo': ultimo_codigo})
    else:
        ultimo_codigo = Produto.objects.latest('codigo').codigo if Produto.objects.exists() else None

        categorias = [choice[0] for choice in Produto.CATEGORIA_CHOICES]
        subcategorias = [choice[0] for choice in Produto.SUB_CHOICES]
        tamanhos = [choice[0] for choice in Produto.TAMANHO_CHOICES]
        return render(request, 'pdv/cadastrar.html', {
            'ultimo_codigo': ultimo_codigo,
            'subcategorias': subcategorias,
            'categorias' : categorias,
            'tamanhos' : tamanhos
            })



def upload_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES['file']
        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)
        for i, row in enumerate(reader):
            try:
                row['empresa'] = request.user.empresa
                Produto.objects.create(**row)
            except Exception as e:
                return JsonResponse({'error': str(e), 'line': i+1}, status=400)
        return HttpResponse("CSV file uploaded and data saved successfully")
    else:
        return HttpResponse("Upload a CSV file")