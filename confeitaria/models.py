from django.db import models
from django.core.validators import MinValueValidator


class Categoria(models.Model):
    nome = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Categoria"

    def __str__(self):
        return self.nome
    
class Doce(models.Model):
    nome = models.CharField(max_length=50, null=False, blank=False)
    descricao = models.TextField(max_length=255, null=False, blank=False)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)  # Vincula o doce a uma categoria
    preco = models.FloatField(null=False, validators=[MinValueValidator(0.10)])
    foto = models.ImageField(upload_to="fotos/%Y/%m/%d/", blank=True)
    estoque = models.PositiveIntegerField(default=0)  # Novo campo para controle de estoque

    def __str__(self):
        return f"{self.nome} - Estoque: {self.estoque}"

