# Sistema de E-commerce Distribuído - Confeitaria

[![Docker](https://img.shields.io/badge/Docker-Ready-blue)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.11-green)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

## 📋 Sobre o Projeto

Sistema de marketplace distribuído para confeitaria, desenvolvido com arquitetura de microserviços como projeto da disciplina **Sistemas Computacionais Distribuídos e Aplicações em Nuvens**.

### Características Principais

- ✅ **Arquitetura de Microserviços**: 3 serviços independentes
- ✅ **Alta Disponibilidade**: Replicação de banco de dados
- ✅ **Escalabilidade Horizontal**: Containers Docker
- ✅ **Tolerância a Falhas**: Failover automático
- ✅ **APIs REST**: Comunicação padronizada
- ✅ **Gerenciamento de Sessões**: Redis cache

## 🏗️ Arquitetura

```
┌──────────────┐
│   Cliente    │
└──────┬───────┘
       │
   ┌───┴───┬─────────────┬──────────┐
   │       │             │          │
┌──▼────┐ ┌▼──────┐ ┌───▼───────┐ ┌▼───────┐
│Catálog│ │Carrin │ │ Catálogo  │ │Pedidos │
│  o    │ │  ho   │ │  Réplica  │ │        │
└──┬────┘ └┬──────┘ └───┬───────┘ └┬───────┘
   │       │            │           │
┌──▼─┐  ┌─▼──┐    ┌────▼──┐   ┌───▼──┐
│PG  │  │Redis│    │ PG    │   │ PG   │
│ DB │  │     │    │Replica│   │ DB   │
└────┘  └─────┘    └───────┘   └──────┘
```

### Microserviços

| Serviço | Porta | Tecnologia | Banco |
|---------|-------|-----------|-------|
| **Catálogo** | 5001 | Flask + SQLAlchemy | PostgreSQL |
| **Catálogo Réplica** | 5011 | Flask + SQLAlchemy | PostgreSQL (Read) |
| **Carrinho** | 5002 | Flask + Redis | Redis |
| **Pedidos** | 5003 | Flask + SQLAlchemy | PostgreSQL |

## 🚀 Início Rápido

### Pré-requisitos

- Docker Desktop 24.x+
- Docker Compose 2.x+
- Git
- 8GB RAM disponível

### Instalação

1. **Clone o repositório**
```powershell
git clone <url-do-repositorio>
cd confeitaria-main
```

2. **Inicie todos os serviços**
```powershell
docker-compose up -d
```

3. **Verifique o status**
```powershell
docker-compose ps
```

4. **Acesse os serviços**
- Catálogo API: http://localhost:5001/api/produtos
- Carrinho API: http://localhost:5002/health
- pgAdmin: http://localhost:5050 (admin@confeitaria.com / admin123)

## 📖 Documentação

- [**Arquitetura Distribuída**](ARQUITETURA_DISTRIBUIDA.md) - Design e conceitos
- [**Guia de Execução**](GUIA_EXECUCAO.md) - Como rodar e testar
- [**Plano de Implementação**](PLANO_IMPLEMENTACAO.md) - Cronograma de 8 semanas
- [**Relatório Técnico**](docs/RELATORIO_TEMPLATE.md) - Template para TCC

## 🧪 Testes

### Teste de Health Check
```powershell
# Catálogo
curl http://localhost:5001/health

# Carrinho
curl http://localhost:5002/health
```

### Teste de Funcionalidade
```powershell
# Listar produtos
curl http://localhost:5001/api/produtos

# Criar sessão de carrinho
$session = Invoke-RestMethod -Uri "http://localhost:5002/api/carrinho/sessao" -Method POST
$sessionId = $session.data.session_id

# Adicionar item
$body = @{produto_id=1; quantidade=2} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:5002/api/carrinho/$sessionId/adicionar" `
    -Method POST -ContentType "application/json" -Body $body
```

### Teste de Tolerância a Falhas
```powershell
# Parar serviço primário
docker-compose stop catalogo-service

# Verificar que réplica continua funcionando
curl http://localhost:5011/api/produtos

# Reiniciar
docker-compose start catalogo-service
```

## 📊 APIs Documentadas

### Serviço de Catálogo

#### Listar Produtos
```http
GET /api/produtos?categoria_id=1&preco_max=50&em_estoque=true
```

**Resposta:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "nome": "Bolo de Chocolate",
      "preco": 45.90,
      "estoque": 10,
      "categoria_nome": "Bolos"
    }
  ],
  "total": 1
}
```

#### Verificar Estoque
```http
GET /api/produtos/1/estoque?quantidade=5
```

#### Atualizar Estoque
```http
PUT /api/produtos/1/estoque
Content-Type: application/json

{
  "quantidade": 10,
  "operacao": "remover"
}
```

### Serviço de Carrinho

#### Criar Sessão
```http
POST /api/carrinho/sessao
```

#### Adicionar Item
```http
POST /api/carrinho/{session_id}/adicionar
Content-Type: application/json

{
  "produto_id": 1,
  "quantidade": 2
}
```

#### Obter Carrinho
```http
GET /api/carrinho/{session_id}
```

## 🛠️ Tecnologias

### Backend
- Python 3.11
- Flask 3.0
- SQLAlchemy 3.1
- Flask-CORS

### Bancos de Dados
- PostgreSQL 15 (ACID, Replicação)
- Redis 7 (Cache, Sessões)

### Infraestrutura
- Docker 24.x
- Docker Compose 2.x
- Nginx (Load Balancer - Opcional)

### Ferramentas de Desenvolvimento
- pgAdmin 4 (Gerenciamento PostgreSQL)
- Redis Commander (Gerenciamento Redis)

## 📈 Conceitos de Sistemas Distribuídos Implementados

### ✅ Transparência
- **Localização**: Cliente não sabe onde serviços estão
- **Replicação**: Réplica transparente ao usuário
- **Acesso**: Interface REST uniforme

### ✅ Escalabilidade
- **Horizontal**: Múltiplas instâncias via Docker
- **Vertical**: Recursos ajustáveis por container

### ✅ Tolerância a Falhas
- **Replicação**: PostgreSQL Master-Slave
- **Health Checks**: Monitoramento de disponibilidade
- **Failover**: Réplica assume quando primário cai

### ✅ Concorrência
- **Redis**: Gerenciamento de múltiplas sessões
- **PostgreSQL**: Isolamento de transações

## 🎯 Requisitos do TCC Atendidos

| Requisito | Status | Implementação |
|-----------|--------|---------------|
| Mínimo 2 serviços | ✅ | Catálogo + Carrinho (+Pedidos) |
| Nós independentes | ✅ | Containers Docker |
| Comunicação REST | ✅ | APIs HTTP/JSON |
| Múltiplos usuários | ✅ | Sessões Redis |
| Replicação | ✅ | PostgreSQL Replica |
| Tolerância a falhas | ✅ | Failover documentado |

## 📁 Estrutura do Projeto

```
confeitaria-main/
├── microservices/
│   ├── catalogo/
│   │   ├── app.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   ├── carrinho/
│   │   ├── app.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   └── pedidos/
│       ├── app.py
│       ├── Dockerfile
│       └── requirements.txt
├── docs/
│   └── RELATORIO_TEMPLATE.md
├── docker-compose.yml
├── ARQUITETURA_DISTRIBUIDA.md
├── GUIA_EXECUCAO.md
├── PLANO_IMPLEMENTACAO.md
└── README.md
```

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

## 📝 Licença

Este projeto é licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👤 Autor

**Paulo H.**
- Disciplina: Sistemas Computacionais Distribuídos
- Instituição: [PREENCHER]
- Ano: 2025

## 📞 Suporte

Para dúvidas ou problemas:
1. Consulte a [documentação](GUIA_EXECUCAO.md)
2. Verifique [issues existentes](../../issues)
3. Abra uma nova issue

## 🎓 Referências

- [Docker Documentation](https://docs.docker.com/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [PostgreSQL Replication](https://www.postgresql.org/docs/current/runtime-config-replication.html)
- [Microservices Patterns](https://microservices.io/patterns/microservices.html)

---

⭐ **Se este projeto foi útil, considere dar uma estrela!**

**Última atualização**: Outubro 2025
