from django.urls import path
from pedidos.views import finalizar_pedido


urlpatterns = [
    path('finalizar', finalizar_pedido, name='finalizar')
]