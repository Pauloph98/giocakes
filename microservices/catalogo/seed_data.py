"""
Script para popular o banco de dados com dados de teste
Execute dentro do container do serviço de catálogo
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import db, Categoria, Produto, app

def popular_dados():
    """Popula banco com categorias e produtos de exemplo"""
    
    with app.app_context():
        # Criar tabelas
        print("Criando tabelas...")
        db.create_all()
        
        # Limpar dados existentes (CUIDADO em produção!)
        print("Limpando dados existentes...")
        Produto.query.delete()
        Categoria.query.delete()
        db.session.commit()
        
        # Criar categorias
        print("Criando categorias...")
        categorias = [
            Categoria(nome='Bolos'),
            Categoria(nome='Doces Finos'),
            Categoria(nome='Tortas'),
            Categoria(nome='Salgados'),
            Categoria(nome='Sobremesas')
        ]
        db.session.add_all(categorias)
        db.session.commit()
        print(f"✓ {len(categorias)} categorias criadas")
        
        # Criar produtos
        print("Criando produtos...")
        produtos = [
            # Bolos
            Produto(
                nome='Bolo de Chocolate',
                descricao='Delicioso bolo de chocolate com cobertura cremosa',
                preco=45.90,
                estoque=10,
                categoria_id=1,
                foto_url='https://via.placeholder.com/300x200?text=Bolo+Chocolate'
            ),
            Produto(
                nome='Bolo de Cenoura',
                descricao='Bolo caseiro de cenoura com cobertura de chocolate',
                preco=38.50,
                estoque=8,
                categoria_id=1,
                foto_url='https://via.placeholder.com/300x200?text=Bolo+Cenoura'
            ),
            Produto(
                nome='Bolo Red Velvet',
                descricao='Bolo aveludado com cream cheese',
                preco=52.00,
                estoque=6,
                categoria_id=1,
                foto_url='https://via.placeholder.com/300x200?text=Red+Velvet'
            ),
            
            # Doces Finos
            Produto(
                nome='Brigadeiro Gourmet',
                descricao='Brigadeiro de chocolate belga (unidade)',
                preco=3.50,
                estoque=100,
                categoria_id=2,
                foto_url='https://via.placeholder.com/300x200?text=Brigadeiro'
            ),
            Produto(
                nome='Beijinho Gourmet',
                descricao='Beijinho com coco fresco (unidade)',
                preco=3.50,
                estoque=100,
                categoria_id=2,
                foto_url='https://via.placeholder.com/300x200?text=Beijinho'
            ),
            Produto(
                nome='Cajuzinho',
                descricao='Doce de amendoim tradicional (unidade)',
                preco=3.00,
                estoque=80,
                categoria_id=2,
                foto_url='https://via.placeholder.com/300x200?text=Cajuzinho'
            ),
            
            # Tortas
            Produto(
                nome='Torta de Limão',
                descricao='Torta cremosa de limão siciliano com merengue',
                preco=38.00,
                estoque=8,
                categoria_id=3,
                foto_url='https://via.placeholder.com/300x200?text=Torta+Limao'
            ),
            Produto(
                nome='Torta de Morango',
                descricao='Torta com creme e morangos frescos',
                preco=42.00,
                estoque=5,
                categoria_id=3,
                foto_url='https://via.placeholder.com/300x200?text=Torta+Morango'
            ),
            Produto(
                nome='Torta Holandesa',
                descricao='Torta gelada com creme e raspas de chocolate',
                preco=45.00,
                estoque=6,
                categoria_id=3,
                foto_url='https://via.placeholder.com/300x200?text=Torta+Holandesa'
            ),
            
            # Salgados
            Produto(
                nome='Coxinha de Frango',
                descricao='Coxinha tradicional (unidade)',
                preco=5.50,
                estoque=50,
                categoria_id=4,
                foto_url='https://via.placeholder.com/300x200?text=Coxinha'
            ),
            Produto(
                nome='Pastel de Carne',
                descricao='Pastel assado recheado (unidade)',
                preco=6.00,
                estoque=40,
                categoria_id=4,
                foto_url='https://via.placeholder.com/300x200?text=Pastel'
            ),
            
            # Sobremesas
            Produto(
                nome='Pudim de Leite',
                descricao='Pudim cremoso com calda de caramelo',
                preco=28.00,
                estoque=10,
                categoria_id=5,
                foto_url='https://via.placeholder.com/300x200?text=Pudim'
            ),
            Produto(
                nome='Mousse de Maracujá',
                descricao='Mousse leve e refrescante',
                preco=25.00,
                estoque=12,
                categoria_id=5,
                foto_url='https://via.placeholder.com/300x200?text=Mousse'
            ),
        ]
        
        db.session.add_all(produtos)
        db.session.commit()
        print(f"✓ {len(produtos)} produtos criados")
        
        # Listar dados criados
        print("\n=== CATEGORIAS CRIADAS ===")
        for cat in Categoria.query.all():
            count = Produto.query.filter_by(categoria_id=cat.id).count()
            print(f"  {cat.id}. {cat.nome} ({count} produtos)")
        
        print("\n=== PRODUTOS CRIADOS ===")
        for prod in Produto.query.all():
            print(f"  {prod.id}. {prod.nome} - R$ {prod.preco:.2f} (Estoque: {prod.estoque})")
        
        print("\n✅ Banco de dados populado com sucesso!")

if __name__ == '__main__':
    popular_dados()
