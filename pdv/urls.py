from django.urls import path
from . import views

urlpatterns = [
    # Logo
    path('logo/<int:empresa_id>', views.serve_logo, name='serve_logo'),

    # Authentication
    path('', views.login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),

    # Payment
    path('pagamento', views.pagamento, name='pagamento'),
    path('resumoCompra/<int:cod>', views.resumoCompra, name='resumoCompra'),
    path('removeCompra/<int:cod>', views.removeCompra, name='removeCompra'),

    # Product management
    path('cadastrar', views.cadastrar, name='cadastrar'),
    path('excluir', views.excluir, name='excluir'),
    path('excluir/<int:id>/', views.itemExcluir, name='itemExcluir'),
    path('editar', views.editar, name='editar'),
    path('editar/<int:id>', views.itemEditar, name='itemEditar'),
    path('itemSelecionado/<int:id>', views.itemSelecionado, name='itemSelecionado'),

    # Sales
    path('registrar_venda', views.registrar_venda, name='registrar_venda'),
    path('vendas', views.renderizar_venda, name='vendas'),

    # CSV
    path('upload_csv', views.upload_csv, name='upload_csv'),
    path('dadosVenda/<int:id>', views.dadosVenda, name='dadosVenda'),

    # Returns
    path('troca/<int:id>', views.efetuar_troca, name='troca'),
    path('codVerify/<int:cod>', views.codVerify, name='codVerify'),
    path('dadosEmpresa/<str:user>', views.dadosEmpresa, name='dadosEmpresa'),

    # Analysis
    path('analise/', views.analise, name='analise'),
    path('analise/getMetodoPagamento', views.getMetodoPagamento, name='getMetodoPagamento'),
    path('analise/getTopProdutosPerHour', views.getTopProdutosPerHour, name='getTopProdutosPerHour'),
    path('analise/getVendasPerHour', views.getVendasPerHour, name='getVendasPerHour'),
    path('analise/getVendasPerVendedor', views.getVendasPerVendedor, name='getVendasPerVendedor'),

    # Cashier
    # path('caixa', views.caixa, name='caixa'),
]