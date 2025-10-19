# Arquitetura Distribuída - Marketplace de Confeitaria
## Projeto TCC: Sistemas Computacionais Distribuídos e Aplicações em Nuvens

---

## 1. VISÃO GERAL DO PROJETO

### Contexto Atual
Seu projeto Django monolítico de confeitaria será transformado em um **marketplace distribuído** com arquitetura de microserviços, atendendo todos os requisitos do TCC.

### Objetivo
Implementar um sistema de e-commerce distribuído, escalável e tolerante a falhas, demonstrando conceitos fundamentais de sistemas distribuídos.

---

## 2. ARQUITETURA PROPOSTA

### 2.1 Microserviços (Decomposição do Monólito)

```
┌─────────────────────────────────────────────────────────────┐
│                    API Gateway (Nginx/Kong)                  │
│                  (Roteamento e Load Balancing)               │
└───────────┬──────────────────┬──────────────────┬───────────┘
            │                  │                  │
    ┌───────▼────────┐  ┌──────▼─────────┐ ┌─────▼──────────┐
    │   Serviço de   │  │   Serviço de   │ │  Serviço de    │
    │    Catálogo    │  │    Carrinho    │ │    Pedidos     │
    │   (Flask/API)  │  │   (Flask/API)  │ │  (Flask/API)   │
    │    Porta 5001  │  │    Porta 5002  │ │   Porta 5003   │
    └───────┬────────┘  └────────┬───────┘ └────────┬────────┘
            │                    │                   │
    ┌───────▼────────┐  ┌────────▼───────┐ ┌────────▼────────┐
    │  PostgreSQL    │  │     Redis      │ │   PostgreSQL    │
    │  (Catálogo DB) │  │  (Sessões)     │ │  (Pedidos DB)   │
    └────────────────┘  └────────────────┘ └─────────────────┘
            │
    ┌───────▼────────┐
    │  PostgreSQL    │
    │ (Réplica Read) │
    └────────────────┘
```

### 2.2 Serviços Detalhados

#### **Serviço 1: Catálogo de Produtos** (OBRIGATÓRIO)
- **Responsabilidade**: Gerenciar produtos, categorias e estoque
- **Tecnologia**: Flask + PostgreSQL
- **Endpoints REST**:
  - `GET /api/produtos` - Listar todos os produtos
  - `GET /api/produtos/{id}` - Detalhes do produto
  - `GET /api/produtos/categoria/{categoria}` - Filtrar por categoria
  - `GET /api/categorias` - Listar categorias
  - `PUT /api/produtos/{id}/estoque` - Atualizar estoque
- **Replicação**: Instância primária (escrita) + réplica secundária (leitura)
- **Porta**: 5001 (primária), 5011 (réplica)

#### **Serviço 2: Carrinho de Compras** (OBRIGATÓRIO)
- **Responsabilidade**: Gerenciar sessões de usuários e carrinhos
- **Tecnologia**: Flask + Redis (cache/sessão)
- **Endpoints REST**:
  - `POST /api/carrinho/adicionar` - Adicionar item
  - `DELETE /api/carrinho/remover/{doce_id}` - Remover item
  - `GET /api/carrinho/{session_id}` - Obter carrinho
  - `DELETE /api/carrinho/{session_id}` - Limpar carrinho
- **Sessão**: Redis para gerenciar estado do usuário
- **Porta**: 5002

#### **Serviço 3: Pedidos** (ADICIONAL - Diferencial)
- **Responsabilidade**: Finalizar pedidos e histórico
- **Tecnologia**: Flask + PostgreSQL
- **Endpoints REST**:
  - `POST /api/pedidos` - Criar pedido
  - `GET /api/pedidos/{id}` - Detalhes do pedido
  - `PUT /api/pedidos/{id}/status` - Atualizar status
- **Integração**: Comunica com Catálogo para validar estoque
- **Porta**: 5003

#### **Frontend (Interface Web)**
- **Tecnologia**: Django (adaptado para consumir APIs)
- **Responsabilidade**: Renderizar templates e servir frontend
- **Porta**: 8000

---

## 3. CONCEITOS DE SISTEMAS DISTRIBUÍDOS APLICADOS

### 3.1 Transparência

| Tipo | Implementação |
|------|---------------|
| **Localização** | API Gateway oculta localização física dos serviços |
| **Replicação** | Catálogo replicado (master-slave) transparente ao cliente |
| **Acesso** | Interface REST uniforme para todos os serviços |
| **Concorrência** | Redis gerencia acesso simultâneo ao carrinho |
| **Falha** | Health checks e retry automático |

### 3.2 Escalabilidade

1. **Horizontal**: Múltiplas instâncias do Catálogo atrás do load balancer
2. **Vertical**: Cada serviço pode escalar independentemente
3. **Elasticidade**: Docker/Kubernetes permite auto-scaling

### 3.3 Tolerância a Falhas

1. **Replicação de Dados**: PostgreSQL com réplica read-only
2. **Circuit Breaker**: Timeout em chamadas entre serviços
3. **Health Checks**: Monitoramento de disponibilidade
4. **Degradação Graciosa**: Se Catálogo cai, réplica assume leitura

### 3.4 Comunicação

- **Síncrona**: REST APIs (HTTP/JSON) entre serviços
- **Assíncrona** (opcional): RabbitMQ para notificações de pedidos
- **Autenticação**: Tokens JWT ou API Keys

---

## 4. TECNOLOGIAS UTILIZADAS

### Backend
- **Python 3.11+** (linguagem base)
- **Flask/FastAPI** (microserviços)
- **Django** (frontend/gateway opcional)

### Bancos de Dados
- **PostgreSQL** (dados transacionais)
- **Redis** (cache e sessões)

### Infraestrutura
- **Docker** (containerização)
- **Docker Compose** (orquestração local)
- **Kubernetes** (orquestração produção - opcional)

### Comunicação
- **REST APIs** (HTTP/JSON)
- **RabbitMQ** (mensageria assíncrona - opcional)

### Monitoramento
- **Prometheus** (métricas)
- **Grafana** (dashboards)
- **ELK Stack** (logs - opcional)

---

## 5. PLANO DE IMPLEMENTAÇÃO

### Fase 1: Preparação (Semana 1)
- [ ] Estruturar repositório Git
- [ ] Configurar ambiente Docker
- [ ] Instalar dependências
- [ ] Criar bancos de dados separados

### Fase 2: Desenvolvimento dos Microserviços (Semanas 2-4)
- [ ] **Serviço de Catálogo**
  - [ ] Migrar models Doce e Categoria para SQLAlchemy
  - [ ] Criar endpoints REST
  - [ ] Implementar réplica PostgreSQL
- [ ] **Serviço de Carrinho**
  - [ ] Implementar sessões com Redis
  - [ ] Criar endpoints REST
  - [ ] Integrar com Catálogo (validação estoque)
- [ ] **Serviço de Pedidos**
  - [ ] Migrar model Pedido
  - [ ] Criar endpoints REST
  - [ ] Integrar com Catálogo (redução estoque)

### Fase 3: Integração (Semana 5)
- [ ] Adaptar frontend Django para consumir APIs
- [ ] Implementar API Gateway/Load Balancer
- [ ] Configurar comunicação entre serviços
- [ ] Implementar autenticação

### Fase 4: Infraestrutura e Deploy (Semana 6)
- [ ] Criar Dockerfiles para cada serviço
- [ ] Criar docker-compose.yml
- [ ] Configurar réplica do Catálogo
- [ ] Deploy em cloud (AWS/GCP/Azure - opcional)

### Fase 5: Testes (Semana 7)
- [ ] Testes de concorrência (múltiplos usuários)
- [ ] Testes de tolerância a falhas (matar containers)
- [ ] Testes de escalabilidade (replicar serviços)
- [ ] Testes de desempenho (Apache Bench/Locust)

### Fase 6: Documentação (Semana 8)
- [ ] Relatório técnico (R.A.)
- [ ] Diagramas de arquitetura
- [ ] Documentação de APIs (Swagger/OpenAPI)
- [ ] Preparação da apresentação

---

## 6. REQUISITOS TÉCNICOS ATENDIDOS

✅ **Mínimo 2 serviços**: Catálogo + Carrinho (+ Pedidos como bônus)  
✅ **Nós independentes**: Cada serviço em container Docker  
✅ **Comunicação REST**: APIs HTTP/JSON entre serviços  
✅ **Múltiplos usuários**: Sessões Redis suportam concorrência  
✅ **Replicação**: Catálogo com réplica PostgreSQL  
✅ **Tolerância a falhas**: Réplica assume se primário cair  

---

## 7. CRITÉRIOS DE AVALIAÇÃO

### Implementação dos Serviços (30%)
- ✅ 3 microserviços funcionais
- ✅ APIs REST bem documentadas
- ✅ Integração entre serviços

### Conceitos de Sistemas Distribuídos (25%)
- ✅ Transparência de localização (API Gateway)
- ✅ Transparência de replicação (Catálogo)
- ✅ Comunicação em rede (REST)
- ✅ Gerenciamento de estado distribuído (Redis)

### Escalabilidade e Tolerância a Falhas (20%)
- ✅ Replicação de Catálogo
- ✅ Testes de falha documentados
- ✅ Health checks implementados
- ✅ Possibilidade de escalar horizontalmente

### Relatório Técnico (15%)
- ✅ Introdução teórica (conceitos SD)
- ✅ Arquitetura detalhada
- ✅ Tecnologias justificadas
- ✅ Resultados de testes
- ✅ Conclusão

### Apresentação (10%)
- ✅ Demonstração ao vivo
- ✅ Explicação da arquitetura
- ✅ Teste de tolerância a falhas

---

## 8. DIFERENCIAIS PARA NOTA MÁXIMA

### Implementações Extras
1. **Mensageria Assíncrona**: RabbitMQ para notificações de pedidos
2. **API Gateway**: Nginx ou Kong para roteamento
3. **Monitoramento**: Prometheus + Grafana
4. **CI/CD**: GitHub Actions para deploy automatizado
5. **Kubernetes**: Deploy em cluster K8s
6. **Service Mesh**: Istio para observabilidade
7. **Testes de Carga**: Locust para simular 1000+ usuários

### Conceitos Avançados
- **Consistência Eventual**: CAP Theorem aplicado
- **Saga Pattern**: Transações distribuídas em pedidos
- **CQRS**: Separação de leitura/escrita no Catálogo
- **Event Sourcing**: Log de eventos de pedidos

---

## 9. CRONOGRAMA SUGERIDO (8 SEMANAS)

| Semana | Atividade | Entregável |
|--------|-----------|------------|
| 1 | Setup e planejamento | Repositório Git, ambiente Docker |
| 2-3 | Desenvolvimento Catálogo | API funcional + réplica |
| 4 | Desenvolvimento Carrinho | API funcional + Redis |
| 5 | Desenvolvimento Pedidos | API funcional + integração |
| 6 | Infraestrutura e Deploy | Docker Compose, containers rodando |
| 7 | Testes e Validação | Relatório de testes |
| 8 | Documentação e Apresentação | Relatório final + slides |

---

## 10. PRÓXIMOS PASSOS

1. **Revisar este documento** com seu orientador
2. **Iniciar Fase 1**: Configurar ambiente
3. **Estudar conceitos**: Microserviços, REST, Docker
4. **Começar código**: Serviço de Catálogo (mais simples)
5. **Documentar progresso**: Commit frequente no Git

---

## 11. RECURSOS E REFERÊNCIAS

### Tutoriais
- Docker: https://docs.docker.com/get-started/
- Flask REST API: https://flask-restful.readthedocs.io/
- PostgreSQL Replication: https://www.postgresql.org/docs/current/runtime-config-replication.html

### Livros
- "Designing Data-Intensive Applications" - Martin Kleppmann
- "Building Microservices" - Sam Newman

### Ferramentas de Teste
- Apache Bench: `ab -n 1000 -c 100 http://localhost:5001/api/produtos`
- Locust: Framework Python para testes de carga

---

**Autor**: Paulo H.  
**Data**: Outubro 2025  
**Disciplina**: Sistemas Computacionais Distribuídos e Aplicações em Nuvens
