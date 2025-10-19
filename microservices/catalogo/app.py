"""
Microserviço de Catálogo de Produtos
Responsável por gerenciar produtos, categorias e estoque
"""
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# Configurações
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL', 
    'postgresql://catalogo_user:catalogo_pass@localhost:5432/catalogo_db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ======================
# MODELS
# ======================

class Categoria(db.Model):
    __tablename__ = 'categorias'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), unique=True, nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    
    produtos = db.relationship('Produto', backref='categoria_rel', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'criado_em': self.criado_em.isoformat() if self.criado_em else None
        }


class Produto(db.Model):
    __tablename__ = 'produtos'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    preco = db.Column(db.Float, nullable=False)
    estoque = db.Column(db.Integer, default=0)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)
    foto_url = db.Column(db.String(255))
    ativo = db.Column(db.Boolean, default=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'preco': self.preco,
            'estoque': self.estoque,
            'categoria_id': self.categoria_id,
            'categoria_nome': self.categoria_rel.nome if self.categoria_rel else None,
            'foto_url': self.foto_url,
            'ativo': self.ativo,
            'criado_em': self.criado_em.isoformat() if self.criado_em else None,
            'atualizado_em': self.atualizado_em.isoformat() if self.atualizado_em else None
        }


# ======================
# ENDPOINTS - CATEGORIAS
# ======================

@app.route('/api/categorias', methods=['GET'])
def listar_categorias():
    """Lista todas as categorias"""
    try:
        categorias = Categoria.query.all()
        return jsonify({
            'success': True,
            'data': [cat.to_dict() for cat in categorias],
            'total': len(categorias)
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/categorias/<int:id>', methods=['GET'])
def obter_categoria(id):
    """Obtém detalhes de uma categoria"""
    try:
        categoria = Categoria.query.get_or_404(id)
        return jsonify({
            'success': True,
            'data': categoria.to_dict()
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 404


# ======================
# ENDPOINTS - PRODUTOS
# ======================

@app.route('/api/produtos', methods=['GET'])
def listar_produtos():
    """
    Lista produtos com filtros opcionais
    Query params: categoria_id, preco_max, em_estoque, busca
    """
    try:
        query = Produto.query.filter_by(ativo=True)
        
        # Filtro por categoria
        categoria_id = request.args.get('categoria_id', type=int)
        if categoria_id:
            query = query.filter_by(categoria_id=categoria_id)
        
        # Filtro por preço máximo
        preco_max = request.args.get('preco_max', type=float)
        if preco_max:
            query = query.filter(Produto.preco <= preco_max)
        
        # Filtro por estoque disponível
        em_estoque = request.args.get('em_estoque', type=bool)
        if em_estoque:
            query = query.filter(Produto.estoque > 0)
        
        # Busca por nome
        busca = request.args.get('busca', type=str)
        if busca:
            query = query.filter(Produto.nome.ilike(f'%{busca}%'))
        
        produtos = query.all()
        
        return jsonify({
            'success': True,
            'data': [prod.to_dict() for prod in produtos],
            'total': len(produtos)
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/produtos/<int:id>', methods=['GET'])
def obter_produto(id):
    """Obtém detalhes de um produto específico"""
    try:
        produto = Produto.query.get_or_404(id)
        return jsonify({
            'success': True,
            'data': produto.to_dict()
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 404


@app.route('/api/produtos/<int:id>/estoque', methods=['GET'])
def verificar_estoque(id):
    """Verifica disponibilidade de estoque"""
    try:
        produto = Produto.query.get_or_404(id)
        quantidade = request.args.get('quantidade', 1, type=int)
        
        disponivel = produto.estoque >= quantidade
        
        return jsonify({
            'success': True,
            'data': {
                'produto_id': produto.id,
                'estoque_atual': produto.estoque,
                'quantidade_solicitada': quantidade,
                'disponivel': disponivel
            }
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 404


@app.route('/api/produtos/<int:id>/estoque', methods=['PUT'])
def atualizar_estoque(id):
    """
    Atualiza estoque de um produto
    Body: {"quantidade": int, "operacao": "adicionar" | "remover" | "definir"}
    """
    try:
        produto = Produto.query.get_or_404(id)
        data = request.get_json()
        
        quantidade = data.get('quantidade', 0)
        operacao = data.get('operacao', 'definir')
        
        if operacao == 'adicionar':
            produto.estoque += quantidade
        elif operacao == 'remover':
            if produto.estoque < quantidade:
                return jsonify({
                    'success': False,
                    'error': 'Estoque insuficiente'
                }), 400
            produto.estoque -= quantidade
        elif operacao == 'definir':
            produto.estoque = quantidade
        else:
            return jsonify({
                'success': False,
                'error': 'Operação inválida'
            }), 400
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': produto.to_dict(),
            'message': f'Estoque atualizado com sucesso'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/produtos/categoria/<int:categoria_id>', methods=['GET'])
def listar_produtos_por_categoria(categoria_id):
    """Lista produtos de uma categoria específica"""
    try:
        categoria = Categoria.query.get_or_404(categoria_id)
        produtos = Produto.query.filter_by(
            categoria_id=categoria_id,
            ativo=True
        ).all()
        
        return jsonify({
            'success': True,
            'data': {
                'categoria': categoria.to_dict(),
                'produtos': [prod.to_dict() for prod in produtos],
                'total': len(produtos)
            }
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 404


# ======================
# HEALTH CHECK
# ======================

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint para verificar saúde do serviço"""
    try:
        # Testa conexão com banco (SQLAlchemy 2.0+ requer text())
        from sqlalchemy import text
        db.session.execute(text('SELECT 1'))
        return jsonify({
            'status': 'healthy',
            'service': 'catalogo',
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'service': 'catalogo',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 503


# ======================
# INICIALIZAÇÃO
# ======================

def criar_tabelas():
    """Cria tabelas ao iniciar a aplicação (se não existirem)"""
    with app.app_context():
        try:
            db.create_all()
            print("✅ Tabelas criadas/verificadas com sucesso")
        except Exception as e:
            print(f"⚠️  Aviso ao criar tabelas: {e}")
            # Continuar mesmo se der erro (tabelas podem já existir)
            pass

# Criar tabelas ao importar o módulo
criar_tabelas()


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    debug = os.getenv('DEBUG', 'True') == 'True'
    app.run(host='0.0.0.0', port=port, debug=debug)
