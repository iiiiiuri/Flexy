from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.hashers import make_password

class User(AbstractUser):
    estoque = models.BooleanField(default=False)
    proprietario = models.BooleanField(default=False)
    vendedor = models.BooleanField(default=False)
    empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE,default=None, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.pk is None:  # This is a new user
            if not self.password.startswith('pbkdf2_sha256$'):  # Check if the password has been hashed
                self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username.capitalize()
    
class Produto(models.Model):
    TAMANHO_CHOICES = [
        ('PP', 'PP'),
        ('P', 'P'),
        ('M', 'M'),
        ('G', 'G'),
        ('GG', 'GG'),
        ('U', 'U'),
    ]
    
    i = 36
    while i <= 70:
        TAMANHO_CHOICES.append((str(i), str(i)))
        i += 1

    CATEGORIA_CHOICES = [
        ('Calçado', 'Calçado'),
        ('Vestuário', 'Vestuário'),
    ]

    SUB_CHOICES = [
        ('Calçado', 'Calçado'),
        ('Conjunto', 'Conjunto'),
        ('Camiseta', 'Camiseta'),
        ('Calça', 'Calça'),
        ('Short', 'Short'),
        ('Blusa', 'Blusa'),
        ('Vestido', 'Vestido'),
        ('Saia', 'Saia'),
        ('Bermuda', 'Bermuda'),
        ('Blazer', 'Blazer'),
        ('Jaqueta', 'Jaqueta'),
        ('Colete', 'Colete'),
        ('Camisa', 'Camisa'),
        ('Regata', 'Regata'),
        ('Macacão', 'Macacão'),
        ('Body', 'Body'),
        ('Top', 'Top'),
        ('Cropped', 'Cropped'),
        ('Sobretudo', 'Sobretudo'),
        ('Suéter', 'Suéter'),
        ('Cardigan', 'Cardigan'),
        ('Poncho', 'Poncho'),
        ('Kimono', 'Kimono'),
        ('Jardineira', 'Jardineira'),
        ('Casaquinho', 'Casaquinho'),
        ('Túnica', 'Túnica'),
    ]

    codigo = models.IntegerField()
    nome = models.CharField(max_length=100)
    cor = models.CharField(max_length=100, null=True, blank=True)
    categoria = models.CharField(max_length=100, choices=CATEGORIA_CHOICES, default='Camiseta')
    subcategoria = models.CharField(max_length=100, choices=SUB_CHOICES ,default='', null=True, blank=True)
    preco = models.FloatField()
    tamanho = models.CharField(max_length=100, choices=TAMANHO_CHOICES, default='U')
    estoque = models.IntegerField()
    empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nome

class ProdutoVendido(models.Model):
    STATUS_CHOICES = [
        ('Finalizada', 'Finalizada'),
        ('Troca Realizada', 'Troca Realizada'),
    ]


    codigo_venda = models.IntegerField()
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    valor_unitario = models.FloatField()
    quantidade = models.IntegerField()
    valor_total = models.FloatField()
    empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='Finalizada')

    def __str__(self):
        return 'Venda: ' + str(self.codigo_venda) + ' - ' + str(self.produto) + ' - ' + str(self.valor_unitario) + ' - ' + str(self.quantidade) + ' - ' + str(self.valor_total)

    def save(self, *args, **kwargs):
        self.valor_total = self.valor_unitario * self.quantidade
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Produtos Vendidos"

class Venda(models.Model):
    codigo = models.IntegerField()
    valor_total = models.FloatField()
    valor_pix = models.FloatField(default=0.0, null=True, blank=True)
    valor_cartao = models.FloatField(default=0.0, null=True, blank=True)
    valor_dinheiro = models.FloatField(default=0.0, null=True, blank=True)
    valor_desconto = models.FloatField(default=0.0, null=True, blank=True)
    vendedor = models.CharField(max_length=100)
    troco = models.FloatField(default=0.0, null=True, blank=True)
    data = models.DateTimeField(auto_now_add=True)
    hora = models.DateTimeField(auto_now_add=True)
    empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return 'Código: ' + str(self.codigo)


class Empresa(models.Model):
    nome = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=100)
    endereco = models.CharField(max_length=100)
    numero = models.CharField(max_length=100)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    celular = models.CharField(max_length=100)
    telefone = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    cep = models.CharField(max_length=100)
    logo = models.FileField(upload_to='logos/', null=True, blank=True)

    def __str__(self):
        return self.nome

class DescontosTroca(models.Model):
    valor_desconto = models.FloatField()
    data = models.DateTimeField(auto_now_add=True)
    empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE, null=True, blank=True)
    codigo_desconto = models.IntegerField()

    def __str__(self):
        return 'Código do Desconto : ' + str(self.codigo_desconto) + ' - Valor do Desconto: ' + str(self.valor_desconto) + ' - Data: ' + str(self.data)

    class Meta:
        verbose_name = "Código de Troca"
        verbose_name_plural = "Códigos de Troca"

# class Caixa(models.Model):
#     STATUS_CHOICES = [
#         ('Aberto', 'Aberto'),
#         ('Fechado', 'Fechado'),
#     ]

#     valor_total = models.FloatField()
#     troco = models.FloatField()
#     data = models.DateTimeField(auto_now_add=True)
#     status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='Aberto')
#     sangria = models.FloatField(default=0.0, null=True, blank=True)
#     operador = models.ForeignKey(User, on_delete=models.CASCADE)
#     empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)

    
#     def clean(self):
#         # Check if the operator is a seller of the same company as the cash register
#         if self.operador.empresa != self.empresa:
#             raise ValidationError("O operador deve ser um vendedor da mesma empresa do caixa.")

#     def save(self, *args, **kwargs):
#         self.full_clean()
#         return super().save(*args, **kwargs)

#     def __str__(self):
#         return 'Valor: ' + str(self.valor) + ' - Data: ' + str(self.data)

#     class Meta:
#         verbose_name = "Caixa"
#         verbose_name_plural = "Caixas"




        