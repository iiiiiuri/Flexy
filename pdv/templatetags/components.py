# pipeline_tags.py
from django import template
from django.core.paginator import Paginator
from pdv.models import User, Produto, Venda
from pdv.views import dicionario_vendas
from datetime import date
from django.db.models import Sum, F



register = template.Library()

@register.inclusion_tag('pdv/components/Alerts/vendaRealizada.html')
def venda_realizada():
    return {}

@register.inclusion_tag('pdv/components/Forms/formVenda.html')
def form_venda():
    return {}

@register.inclusion_tag('pdv/components/Forms/formSelectVendedor.html')
def form_select_vendedor(request):
    vendedores = User.objects.filter(vendedor=True, empresa=request.user.empresa)
    return {'vendedores': vendedores}


@register.inclusion_tag('pdv/components/Headings/title.html')
def title(title):
    return {'title': title}

@register.inclusion_tag('pdv/components/Input Fields/searchBar.html')
def search_bar():
    return {}

@register.inclusion_tag('pdv/components/Tables/tableProdutos.html')
def table_produtos(request):
    produtos = Produto.objects.filter(empresa=request.user.empresa).exclude(estoque=0)
    return {'produtos': produtos}

@register.inclusion_tag('pdv/components/Alerts/noResults.html')
def no_results():
    return {}

@register.inclusion_tag('pdv/components/Forms/formDevolucao.html')
def form_devolucao():
    return {}

@register.inclusion_tag('pdv/components/Tables/tableVendas.html')
def table_vendas(request):
    vendas = dicionario_vendas(request)
    paginator = Paginator(vendas, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return {'vendas': page_obj}


@register.inclusion_tag('pdv/components/Forms/formTroca.html')
def form_troca():
    return {}

@register.inclusion_tag('pdv/components/Flowbite/Charts/pieChart.html')
def pie():
    return {}

@register.inclusion_tag('pdv/components/Flowbite/Charts/barChart.html')
def bar():
    return {}

@register.inclusion_tag('pdv/components/Flowbite/Charts/linesChart.html')
def line(request):
    total_vendas_hoje = Venda.objects.filter(data__date=date.today(), empresa=request.user.empresa).aggregate(
        total=Sum(F('valor_dinheiro') + F('valor_pix') + F('valor_cartao') + F('valor_desconto'))
    )['total']
    total_vendas_hoje = round(total_vendas_hoje, 2) if total_vendas_hoje else 0
    return {'totalVendasHoje': total_vendas_hoje if total_vendas_hoje else 0}

@register.inclusion_tag('pdv/components/Flowbite/Charts/horizontalChart.html')
def horizontal():
    return {}