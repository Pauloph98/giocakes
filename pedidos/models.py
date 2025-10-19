from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from datetime import timedelta
from confeitaria.models import Doce

def data_retirada_padrao():
    return timezone.now() + timedelta(days=2)  # Ajuste para 2 dias ou qualquer valor desejado

class Pedido(models.Model):
    nome_comprador = models.CharField(max_length=60, null=False, blank=False)
    contato_comprador = models.CharField(max_length=20, null=False, blank=False)
    nome_retirada = models.CharField(max_length=60, null=True, blank=True) 
    data_retirada = models.DateField(default=data_retirada_padrao)
    mensagem = models.TextField(blank=True, null=True, max_length=255)
    data_pedido = models.DateField(default=timezone.now)
    itens = models.ManyToManyField(Doce, through='PedidoItem')

    # Campos adicionais
    valor_total = models.FloatField(default=0.0)
    entregue = models.BooleanField(default=False)
    data_entrega = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Pedido {self.id} por {self.nome_comprador}"

class PedidoItem(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    doce = models.ForeignKey(Doce, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantidade} x {self.doce.nome} no pedido {self.pedido.id}"
