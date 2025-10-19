from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from confeitaria.models import Doce
from pedidos.models import Pedido, PedidoItem
from pedidos.forms import PedidoForms
import urllib.parse

def finalizar_pedido(request):
    itens = request.session.get('Carrinho', [])
    if not itens:
        messages.error(request, 'Seu carrinho está vazio!')
        return redirect('carrinho')

    # Carregar os doces do carrinho, verificando se cada item existe
    doces = []
    for item in itens:
        try:
            doce = get_object_or_404(Doce, pk=item['doce_id'])  # Acessa o doce_id corretamente
            if doce.estoque <= 0:
                messages.error(request, f"O doce '{doce.nome}' está fora de estoque.")
                return redirect('carrinho')
            doces.append({'doce': doce, 'quantidade': item['quantidade']})  # Inclui a quantidade também
        except Exception as e:
            messages.error(request, f"Ocorreu um problema ao processar o item de ID {item['doce_id']}.")
            return redirect('carrinho')

    # Cálculo do valor total do pedido
    valor_total = sum(doce['doce'].preco * doce['quantidade'] for doce in doces)
    form = PedidoForms()

    if request.method == 'POST':
        form = PedidoForms(request.POST)
        if form.is_valid():
            # Salva informações do pedido
            nome = form.cleaned_data['nome']
            telefone = form.cleaned_data['telefone']
            nome_retirada = form.cleaned_data['nome_retirada']
            data_retirada = form.cleaned_data['data_retirada']
            mensagem = form.cleaned_data['mensagem']

            # Cria o pedido com o valor total calculado
            pedido = Pedido.objects.create(
                nome_comprador=nome,
                contato_comprador=telefone,
                nome_retirada=nome_retirada,
                data_retirada=data_retirada,
                mensagem=mensagem,
                valor_total=valor_total
            )

            # Adicionar itens ao pedido e reduzir estoque
            for doce_info in doces:
                doce = doce_info['doce']
                quantidade = doce_info['quantidade']
                PedidoItem.objects.create(pedido=pedido, doce=doce, quantidade=quantidade)
                doce.estoque -= quantidade
                doce.save()

            # Limpar o carrinho após finalizar o pedido
            request.session['Carrinho'] = []

            # Preparar mensagem para WhatsApp
            itens_texto = "\n".join([f"- {doce_info['doce'].nome} (Quantidade: {doce_info['quantidade']})" for doce_info in doces])
            texto_whatsapp = f"""
                *Pedido para Retirada*
                Nome do Cliente: {nome}
                Telefone: {telefone}
                Nome de quem irá Retirar: {nome_retirada}
                Data para Retirada: {data_retirada.strftime('%d/%m/%Y')}
                Mensagem: {mensagem if mensagem else "Nenhuma observação adicional"}
                Valor Total: R${valor_total:.2f}

                *Itens do Pedido:*
                {itens_texto}
            """
            texto_whatsapp = urllib.parse.quote(texto_whatsapp)
            url_whatsapp = f"https://wa.me/5562996877578?text={texto_whatsapp}"

            messages.success(request, 'Pedido finalizado com sucesso! Você será redirecionado para o WhatsApp.')
            return redirect(url_whatsapp)

    return render(request, "pedidos/finalizar-pedido.html", {"form": form, "valor_total": valor_total})
