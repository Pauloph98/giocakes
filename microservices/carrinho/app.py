"""
Microserviço de Carrinho de Compras
Responsável por gerenciar sessões de usuários e itens do carrinho
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
import redis
import json
import os
import requests
from datetime import datetime, timedelta
import uuid

app = Flask(__name__)
CORS(app)

# Configurações Redis
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_DB = int(os.getenv('REDIS_DB', 0))
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', None)

# URL do serviço de catálogo
CATALOGO_URL = os.getenv('CATALOGO_URL', 'http://localhost:5001')

# Conexão Redis
redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    password=REDIS_PASSWORD,
    decode_responses=True
)

# Tempo de expiração do carrinho (24 horas)
CARRINHO_TTL = 86400


# ======================
# FUNÇÕES AUXILIARES
# ======================

def gerar_session_id():
    """Gera um ID de sessão único"""
    return str(uuid.uuid4())


def validar_produto_catalogo(produto_id, quantidade):
    """Valida disponibilidade do produto no serviço de catálogo"""
    try:
        response = requests.get(
            f'{CATALOGO_URL}/api/produtos/{produto_id}/estoque',
            params={'quantidade': quantidade},
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            return data.get('data', {}).get('disponivel', False)
        return False
    except Exception as e:
        print(f"Erro ao validar produto: {e}")
        return False


def obter_detalhes_produto(produto_id):
    """Obtém detalhes do produto do serviço de catálogo"""
    try:
        response = requests.get(
            f'{CATALOGO_URL}/api/produtos/{produto_id}',
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            return data.get('data')
        return None
    except Exception as e:
        print(f"Erro ao obter produto: {e}")
        return None


def get_carrinho(session_id):
    """Obtém carrinho do Redis"""
    carrinho_json = redis_client.get(f'carrinho:{session_id}')
    if carrinho_json:
        return json.loads(carrinho_json)
    return {'itens': [], 'criado_em': datetime.utcnow().isoformat()}


def salvar_carrinho(session_id, carrinho):
    """Salva carrinho no Redis com TTL"""
    carrinho['atualizado_em'] = datetime.utcnow().isoformat()
    redis_client.setex(
        f'carrinho:{session_id}',
        CARRINHO_TTL,
        json.dumps(carrinho)
    )


# ======================
# ENDPOINTS
# ======================

@app.route('/api/carrinho/sessao', methods=['POST'])
def criar_sessao():
    """Cria uma nova sessão de carrinho"""
    try:
        session_id = gerar_session_id()
        carrinho = {
            'itens': [],
            'criado_em': datetime.utcnow().isoformat(),
            'atualizado_em': datetime.utcnow().isoformat()
        }
        salvar_carrinho(session_id, carrinho)
        
        return jsonify({
            'success': True,
            'data': {
                'session_id': session_id,
                'expira_em': (datetime.utcnow() + timedelta(seconds=CARRINHO_TTL)).isoformat()
            }
        }), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/carrinho/<session_id>', methods=['GET'])
def obter_carrinho(session_id):
    """Obtém carrinho de uma sessão"""
    try:
        carrinho = get_carrinho(session_id)
        
        # Enriquece itens com dados do catálogo
        itens_enriquecidos = []
        valor_total = 0
        
        for item in carrinho['itens']:
            produto = obter_detalhes_produto(item['produto_id'])
            if produto:
                item_enriquecido = {
                    **item,
                    'produto': produto,
                    'subtotal': produto['preco'] * item['quantidade']
                }
                itens_enriquecidos.append(item_enriquecido)
                valor_total += item_enriquecido['subtotal']
        
        return jsonify({
            'success': True,
            'data': {
                'session_id': session_id,
                'itens': itens_enriquecidos,
                'total_itens': len(itens_enriquecidos),
                'valor_total': valor_total,
                'criado_em': carrinho.get('criado_em'),
                'atualizado_em': carrinho.get('atualizado_em')
            }
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/carrinho/<session_id>/adicionar', methods=['POST'])
def adicionar_item(session_id):
    """
    Adiciona item ao carrinho
    Body: {"produto_id": int, "quantidade": int}
    """
    try:
        data = request.get_json()
        produto_id = data.get('produto_id')
        quantidade = data.get('quantidade', 1)
        
        if not produto_id or quantidade <= 0:
            return jsonify({
                'success': False,
                'error': 'produto_id e quantidade são obrigatórios'
            }), 400
        
        # Valida disponibilidade no catálogo
        if not validar_produto_catalogo(produto_id, quantidade):
            return jsonify({
                'success': False,
                'error': 'Produto indisponível ou estoque insuficiente'
            }), 400
        
        # Obtém carrinho atual
        carrinho = get_carrinho(session_id)
        
        # Verifica se produto já está no carrinho
        item_existente = None
        for item in carrinho['itens']:
            if item['produto_id'] == produto_id:
                item_existente = item
                break
        
        if item_existente:
            # Atualiza quantidade
            nova_quantidade = item_existente['quantidade'] + quantidade
            if not validar_produto_catalogo(produto_id, nova_quantidade):
                return jsonify({
                    'success': False,
                    'error': 'Quantidade total excede estoque disponível'
                }), 400
            item_existente['quantidade'] = nova_quantidade
        else:
            # Adiciona novo item
            carrinho['itens'].append({
                'produto_id': produto_id,
                'quantidade': quantidade,
                'adicionado_em': datetime.utcnow().isoformat()
            })
        
        salvar_carrinho(session_id, carrinho)
        
        return jsonify({
            'success': True,
            'message': 'Item adicionado ao carrinho',
            'data': carrinho
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/carrinho/<session_id>/remover/<int:produto_id>', methods=['DELETE'])
def remover_item(session_id, produto_id):
    """Remove item do carrinho"""
    try:
        carrinho = get_carrinho(session_id)
        
        # Remove item
        carrinho['itens'] = [
            item for item in carrinho['itens'] 
            if item['produto_id'] != produto_id
        ]
        
        salvar_carrinho(session_id, carrinho)
        
        return jsonify({
            'success': True,
            'message': 'Item removido do carrinho',
            'data': carrinho
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/carrinho/<session_id>/atualizar/<int:produto_id>', methods=['PUT'])
def atualizar_quantidade(session_id, produto_id):
    """
    Atualiza quantidade de um item
    Body: {"quantidade": int}
    """
    try:
        data = request.get_json()
        quantidade = data.get('quantidade', 1)
        
        if quantidade <= 0:
            return jsonify({
                'success': False,
                'error': 'Quantidade deve ser maior que zero'
            }), 400
        
        # Valida disponibilidade
        if not validar_produto_catalogo(produto_id, quantidade):
            return jsonify({
                'success': False,
                'error': 'Estoque insuficiente'
            }), 400
        
        carrinho = get_carrinho(session_id)
        
        # Atualiza quantidade
        item_encontrado = False
        for item in carrinho['itens']:
            if item['produto_id'] == produto_id:
                item['quantidade'] = quantidade
                item_encontrado = True
                break
        
        if not item_encontrado:
            return jsonify({
                'success': False,
                'error': 'Item não encontrado no carrinho'
            }), 404
        
        salvar_carrinho(session_id, carrinho)
        
        return jsonify({
            'success': True,
            'message': 'Quantidade atualizada',
            'data': carrinho
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/carrinho/<session_id>', methods=['DELETE'])
def limpar_carrinho(session_id):
    """Limpa carrinho completamente"""
    try:
        redis_client.delete(f'carrinho:{session_id}')
        
        return jsonify({
            'success': True,
            'message': 'Carrinho limpo com sucesso'
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ======================
# HEALTH CHECK
# ======================

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint para verificar saúde do serviço"""
    try:
        # Testa conexão Redis
        redis_client.ping()
        
        # Testa conexão com catálogo
        catalogo_response = requests.get(f'{CATALOGO_URL}/health', timeout=2)
        catalogo_healthy = catalogo_response.status_code == 200
        
        return jsonify({
            'status': 'healthy',
            'service': 'carrinho',
            'redis': 'connected',
            'catalogo': 'connected' if catalogo_healthy else 'disconnected',
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'service': 'carrinho',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 503


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5002))
    debug = os.getenv('DEBUG', 'True') == 'True'
    app.run(host='0.0.0.0', port=port, debug=debug)
