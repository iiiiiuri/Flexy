from django.contrib import admin
from .models import User, Produto, Venda, ProdutoVendido, Empresa, DescontosTroca

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'empresa')
    search_fields = ('username', 'email', 'empresa')
    list_filter = ('is_staff', 'empresa')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(empresa=request.user.empresa)

class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'empresa')
    search_fields = ('nome', 'empresa')
    list_filter = ('preco', 'empresa')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(empresa=request.user.empresa)

class ProdutoVendidoAdmin(admin.ModelAdmin):
    list_display = ('codigo_venda', 'produto', 'quantidade', 'empresa')
    search_fields = ('codigo_venda', 'produto', 'empresa')
    list_filter = ('produto', 'empresa')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(empresa=request.user.empresa)

class VendaAdmin(admin.ModelAdmin):
    list_display = ('id', 'data', 'valor_total', 'empresa')
    search_fields = ('id', 'empresa')
    list_filter = ('data', 'empresa')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(empresa=request.user.empresa)

class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cnpj')
    search_fields = ('nome', 'cnpj')
    list_filter = ('nome',)

class DescontosTrocaAdmin(admin.ModelAdmin):
    list_display = ('codigo_desconto','valor_desconto', 'data', 'empresa')
    list_filter = ('data', 'empresa')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(empresa=request.user.empresa)

class CaixaAdmin(admin.ModelAdmin):
    list_display = ('data', 'valor_total', 'status', 'sangria', 'operador', 'empresa', 'valor_total')
    search_fields = ('data', 'valor_total', 'status', 'sangria', 'operador__username', 'empresa__nome')

# admin.site.register(Caixa, CaixaAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Produto, ProdutoAdmin)
admin.site.register(ProdutoVendido, ProdutoVendidoAdmin)
admin.site.register(Venda, VendaAdmin)
admin.site.register(Empresa, EmpresaAdmin)
admin.site.register(DescontosTroca, DescontosTrocaAdmin)

admin.site.site_header = "Flexy Admin"
admin.site.site_title = "Flexy Admin Portal"
admin.site.index_title = "Welcome to Flexy Portal"