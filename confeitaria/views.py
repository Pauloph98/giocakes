from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from confeitaria.models import Doce, Categoria

from django.shortcuts import render, get_object_or_404
from confeitaria.models import Doce, Categoria  # Corrigido para Categoria

# Em views.py
# Em views.py
def index(request):
    # Obter doces abaixo de 20 reais
    doces_baratos = Doce.objects.filter(preco__lt=20.0)

    # Obter a categoria da URL ou definir "TODOS" como padrão
    categoria_slug = request.GET.get('categoria', 'TODOS')

    if categoria_slug == 'TODOS':
        doces = Doce.objects.all()  # Removemos o limite de 10
    else:
        categoria = get_object_or_404(Categoria, nome=categoria_slug)
        doces = Doce.objects.filter(categoria=categoria)  # Filtro sem limite

    # Carregar todas as categorias, incluindo a opção "TODOS"
    categorias = Categoria.objects.all()
    
    # Incluindo "TODOS" como a primeira opção
    categorias_com_todos = [None] + list(categorias)  # None representa a opção "TODOS"

    return render(request, "confeitaria/index.html", {
        "doces": doces,
        "doces_baratos": doces_baratos,
        "categorias": categorias_com_todos,  # Passando a lista de categorias com "TODOS"
        "categoria_selecionada": categoria_slug
    })



def busca(request):
    if request.method != 'POST' or 'busca' not in request.POST:
        return redirect('index')
    
    query = request.POST['busca']
    doces = Doce.objects.filter(nome__icontains=query)
    return render(request, 'confeitaria/busca.html', {"doces": doces, "busca": query})

def detalhes_doce(request, doce_id):
    doce = get_object_or_404(Doce, pk=doce_id)
    doces_relacionados = Doce.objects.filter(categoria=doce.categoria)[:10]
    return render(request, 'confeitaria/detalhes.html', {
        "doce": doce,
        "doces_relacionados": [d for d in doces_relacionados if d.id != doce_id]
    })

def carrinho(request):
    if request.method == 'POST':
        tipo = request.POST.get('tipo')
        doce_id = request.POST.get('doce_id')
        quantidade = int(request.POST.get('quantidade', 1))  # Pega a quantidade, com valor padrão de 1

        if tipo == 'limpar':
            # Limpa o carrinho e redireciona sem tentar acessar itens
            request.session['Carrinho'] = []
            messages.success(request, "Carrinho limpo com sucesso!")
            return redirect('carrinho')  # Redireciona para evitar erros de referência a itens inexistentes

        # Obtenha o objeto Doce para verificar o estoque
        doce = get_object_or_404(Doce, pk=doce_id)

        if tipo == 'adicionar':
            # Adiciona ou atualiza o carrinho
            if 'Carrinho' not in request.session:
                request.session['Carrinho'] = []

            carrinho = request.session['Carrinho']
            item_existente = next((item for item in carrinho if item['doce_id'] == doce_id), None)

            # Verificar se a quantidade no carrinho não ultrapassa o estoque
            if item_existente:
                nova_quantidade = item_existente['quantidade'] + quantidade
                if nova_quantidade > doce.estoque:
                    messages.error(request, f"Estoque insuficiente para {doce.nome}. Estoque disponível: {doce.estoque}.")
                    return redirect('carrinho')
                item_existente['quantidade'] = nova_quantidade
            else:
                if quantidade > doce.estoque:
                    messages.error(request, f"Estoque insuficiente para {doce.nome}. Estoque disponível: {doce.estoque}.")
                    return redirect('carrinho')
                carrinho.append({'doce_id': doce_id, 'quantidade': quantidade})

            request.session['Carrinho'] = carrinho
            messages.success(request, "Doce adicionado ao carrinho com sucesso!")

        elif tipo == 'remover':
            itens = request.session.get('Carrinho', [])
            for item in itens:
                if item['doce_id'] == doce_id:
                    itens.remove(item)
                    break
            request.session['Carrinho'] = itens
            messages.success(request, "Doce removido do carrinho com sucesso!")

        return redirect('carrinho')  # Redireciona para atualizar a página do carrinho

    # Código GET para exibir o carrinho
    elif request.method == 'GET':
        itens = request.session.get('Carrinho', [])
        doces = []
        valor_total = 0
        for item in itens:
            doce = get_object_or_404(Doce, pk=item['doce_id'])
            total_item = doce.preco * item['quantidade']
            doces.append({'doce': doce, 'quantidade': item['quantidade'], 'total_item': total_item})
            valor_total += total_item

        return render(request, 'confeitaria/carrinho.html', {"itens": doces, "valor_total": valor_total})


def erro404(request, exception):
    return render(request, 'erro.html', {"mensagem": "Ops! A página que você buscou não foi encontrada =("}, status=404)

def erro500(request):
    return render(request, 'erro.html', {"mensagem": "Ops! Aconteceu um erro inesperado no nosso servidor =("}, status=500)
