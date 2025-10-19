from django.contrib import admin
from pedidos.models import Pedido, PedidoItem

# Define o inline para exibir itens do pedido com a quantidade
class PedidoItemInline(admin.TabularInline):
    model = PedidoItem
    extra = 0  # Remove linhas adicionais vazias
    readonly_fields = ('doce', 'quantidade')  # Campos somente leitura para evitar edição acidental

class PedidoAdmin(admin.ModelAdmin):
    list_display = ('nome_comprador', 'contato_comprador', 'nome_retirada', 'data_retirada', 'valor_total', 'entregue')
    list_display_links = ('nome_comprador', 'data_retirada')
    search_fields = ('nome_comprador', 'nome_retirada')
    list_filter = ('entregue', 'data_retirada')
    
    # Adiciona o inline para exibir itens do pedido
    inlines = [PedidoItemInline]

admin.site.register(Pedido, PedidoAdmin)