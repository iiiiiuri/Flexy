from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def login(request):
    if request.method == 'POST':
        username = request.POST['usuario']
        password = request.POST['senha']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user) 
            return redirect('pagamento')
        else:
            return render(request, 'pdv/login.html', {'error': 'Usuário ou senha inválidos'})
    else:
        return render(request, 'pdv/login.html')
    
@login_required
def register(request):

    if not request.user.proprietario:
            return redirect('pagamento')

    if request.method == 'POST':
        username = request.POST['usuario']
        password = request.POST['senha']
        password2 = request.POST['senha2']
        estoque = request.POST.get('estoque')
        vendedor = request.POST.get('vendedor')


        User = get_user_model()
        if User.objects.filter(username=username).exists():
            return render(request, 'pdv/register.html', {'error': 'Usuário já existe'})

        if password != password2:
            return render(request, 'pdv/register.html', {'error': 'Senhas não coincidem'})

        if estoque not in ['true', 'false']:
            return render(request, 'pdv/register.html', {'error': 'Estoque inválido'})

        estoque = estoque == 'true'

        if vendedor not in ['true', 'false']:
            return render(request, 'pdv/register.html', {'error': 'Vendedor inválido'})

        vendedor = vendedor == 'true'

        try:
            user = User.objects.create_user(username=username, password=password, estoque=estoque, vendedor=vendedor)
            user.save()
        except Exception as e:
            return render(request, 'pdv/register.html', {'error': str(e)})

        messages.success(request, 'Registro concluido com sucesso')
        return redirect('login')

    return render(request, 'pdv/register.html')
    
def logout(request):
    auth_logout(request)
    return redirect('login')
    
