# Script para popular PostgreSQL com dados do sistema
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from confeitaria.models import Categoria, Doce

# Criar categorias
categorias_data = [
    {"nome": "Bolos"},
    {"nome": "Tortas"},
    {"nome": "Docinhos"},
    {"nome": "Salgados"},
    {"nome": "Bebidas"}
]

print("Criando categorias...")
for cat_data in categorias_data:
    cat, created = Categoria.objects.get_or_create(nome=cat_data["nome"])
    if created:
        print(f"  ✅ {cat.nome}")
    else:
        print(f"  ⚠️  {cat.nome} já existe")

print(f"\nTotal de categorias: {Categoria.objects.count()}")

# Criar alguns doces de exemplo
print("\nCriando doces de exemplo...")

doces_exemplo = [
    {
        "nome": "Brigadeiro Gourmet",
        "preco": 3.50,
        "descricao": "Brigadeiro tradicional com chocolate belga",
        "categoria": Categoria.objects.get(nome="Docinhos"),
        "estoque": 100
    },
    {
        "nome": "Bolo de Chocolate",
        "preco": 45.00,
        "descricao": "Bolo de chocolate com cobertura de ganache",
        "categoria": Categoria.objects.get(nome="Bolos"),
        "estoque": 10
    },
    {
        "nome": "Torta de Morango",
        "preco": 55.00,
        "descricao": "Torta com creme e morangos frescos",
        "categoria": Categoria.objects.get(nome="Tortas"),
        "estoque": 8
    },
    {
        "nome": "Coxinha",
        "preco": 5.00,
        "descricao": "Coxinha de frango tradicional",
        "categoria": Categoria.objects.get(nome="Salgados"),
        "estoque": 50
    },
    {
        "nome": "Suco Natural",
        "preco": 8.00,
        "descricao": "Suco de laranja natural",
        "categoria": Categoria.objects.get(nome="Bebidas"),
        "estoque": 20
    }
]

for doce_data in doces_exemplo:
    doce, created = Doce.objects.get_or_create(
        nome=doce_data["nome"],
        defaults=doce_data
    )
    if created:
        print(f"  ✅ {doce.nome} - R$ {doce.preco}")
    else:
        print(f"  ⚠️  {doce.nome} já existe")

print(f"\nTotal de doces: {Doce.objects.count()}")
print("\n✅ Banco de dados populado com sucesso!")
