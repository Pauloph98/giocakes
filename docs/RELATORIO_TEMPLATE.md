# 📚 Relatório Técnico - Template para TCC

## Marketplace Distribuído em Nuvem com Microserviços
### Sistema de E-commerce de Confeitaria

---

**Disciplina**: Sistemas Computacionais Distribuídos e Aplicações em Nuvens  
**Aluno**: Paulo H.  
**Data**: [PREENCHER]  
**Instituição**: [PREENCHER]  

---

## RESUMO

Este trabalho apresenta a implementação de um marketplace distribuído utilizando arquitetura de microserviços, com foco em escalabilidade, disponibilidade e tolerância a falhas. O sistema foi desenvolvido para gerenciar um e-commerce de confeitaria, decomposto em três serviços independentes: Catálogo de Produtos, Carrinho de Compras e Pedidos. A solução utiliza tecnologias modernas como Flask, PostgreSQL, Redis e Docker, implementando conceitos fundamentais de sistemas distribuídos como transparência, replicação e comunicação em rede.

**Palavras-chave**: Sistemas Distribuídos, Microserviços, REST API, Docker, Replicação, Tolerância a Falhas.

---

## 1. INTRODUÇÃO

### 1.1 Contexto

Os sistemas distribuídos são fundamentais para aplicações modernas que exigem alta disponibilidade, escalabilidade e desempenho. Segundo Tanenbaum e Van Steen (2017), um sistema distribuído é "uma coleção de computadores independentes que aparecem ao usuário como um único sistema coerente". Esta definição captura a essência da transparência, um dos pilares dos sistemas distribuídos.

No contexto de e-commerce, marketplaces online enfrentam desafios únicos:
- **Escalabilidade**: necessidade de suportar milhares de usuários simultâneos
- **Disponibilidade**: sistemas devem estar online 24/7
- **Consistência**: dados de estoque devem ser sincronizados
- **Desempenho**: respostas rápidas são críticas para experiência do usuário

### 1.2 Motivação

O desenvolvimento de um marketplace de confeitaria como sistema distribuído permite:
1. Aplicar conceitos teóricos da disciplina em cenário prático
2. Compreender trade-offs entre consistência, disponibilidade e particionamento (CAP Theorem)
3. Implementar padrões de arquitetura de microserviços
4. Explorar tecnologias de containerização e orquestração

### 1.3 Objetivos

#### Objetivo Geral
Projetar e implementar um marketplace distribuído utilizando arquitetura de microserviços, garantindo escalabilidade, disponibilidade e tolerância a falhas.

#### Objetivos Específicos
1. Decompor aplicação monolítica em microserviços independentes
2. Implementar comunicação REST entre serviços
3. Configurar replicação de banco de dados para alta disponibilidade
4. Testar tolerância a falhas através de simulações
5. Avaliar desempenho em cenários de múltiplos usuários concorrentes

### 1.4 Estrutura do Trabalho

Este relatório está organizado da seguinte forma:
- **Seção 2**: Fundamentação teórica sobre sistemas distribuídos
- **Seção 3**: Arquitetura proposta e decisões de design
- **Seção 4**: Detalhes de implementação
- **Seção 5**: Metodologia e resultados dos testes
- **Seção 6**: Discussão e análise
- **Seção 7**: Conclusão e trabalhos futuros

---

## 2. FUNDAMENTAÇÃO TEÓRICA

### 2.1 Sistemas Distribuídos

#### 2.1.1 Definição e Características

Um sistema distribuído é caracterizado por (COULOURIS et al., 2013):
- **Concorrência**: múltiplos processos executam simultaneamente
- **Ausência de relógio global**: sincronização é desafiadora
- **Falhas independentes**: componentes podem falhar separadamente

#### 2.1.2 Transparência

A transparência visa ocultar do usuário a complexidade da distribuição:

| Tipo | Descrição | Aplicação no Projeto |
|------|-----------|---------------------|
| **Localização** | Oculta onde recursos estão fisicamente | API Gateway oculta localização dos serviços |
| **Replicação** | Oculta existência de cópias | Catálogo replicado sem conhecimento do cliente |
| **Acesso** | Oculta diferenças de acesso | Interface REST uniforme |
| **Concorrência** | Oculta acesso simultâneo | Redis gerencia locks de sessão |
| **Falha** | Oculta falhas e recuperação | Failover automático para réplica |

#### 2.1.3 CAP Theorem

O teorema CAP (Brewer, 2000) afirma que em sistemas distribuídos é impossível garantir simultaneamente:
- **Consistency** (Consistência): todos os nós veem os mesmos dados
- **Availability** (Disponibilidade): sistema sempre responde
- **Partition Tolerance** (Tolerância a partições): sistema funciona mesmo com falhas de rede

**Escolha do Projeto**: CP (Consistência + Particionamento)
- Catálogo: prioriza consistência de estoque
- Carrinho: prioriza disponibilidade (eventual consistency)

### 2.2 Arquitetura de Microserviços

#### 2.2.1 Conceito

Microserviços são "serviços pequenos, autônomos que trabalham juntos" (NEWMAN, 2015). Características:
- Responsabilidade única (Single Responsibility Principle)
- Deploy independente
- Banco de dados por serviço
- Comunicação via protocolos leves (HTTP/REST)

#### 2.2.2 Vantagens
- **Escalabilidade independente**: cada serviço escala conforme necessidade
- **Tecnologias heterogêneas**: cada serviço pode usar stack diferente
- **Resiliência**: falha de um serviço não derruba todo sistema
- **Facilidade de deploy**: mudanças menores e mais frequentes

#### 2.2.3 Desvantagens
- **Complexidade operacional**: mais componentes para gerenciar
- **Comunicação em rede**: latência e falhas de rede
- **Consistência distribuída**: transações ACID são complexas
- **Testes**: testes de integração mais difíceis

### 2.3 REST APIs

REST (Representational State Transfer) é um estilo arquitetural para sistemas distribuídos:

**Princípios REST**:
1. **Stateless**: servidor não mantém estado do cliente
2. **Cliente-Servidor**: separação de responsabilidades
3. **Cacheable**: respostas devem indicar se são cacheáveis
4. **Interface Uniforme**: URIs padronizadas e métodos HTTP

**Métodos HTTP**:
- `GET`: recuperar recurso
- `POST`: criar recurso
- `PUT`: atualizar recurso
- `DELETE`: remover recurso

### 2.4 Replicação de Dados

#### 2.4.1 Tipos de Replicação

**Master-Slave (Primary-Replica)**:
- Escritas apenas no master
- Leituras distribuídas em replicas
- Usado no serviço de Catálogo

**Multi-Master**:
- Escritas em qualquer nó
- Conflitos devem ser resolvidos
- Maior complexidade

#### 2.4.2 Consistência

**Consistência Forte**: todos os nós sempre retornam o mesmo valor
**Consistência Eventual**: nós convergem para o mesmo estado após tempo

### 2.5 Containerização

**Docker** permite empacotar aplicações com todas as dependências em containers:
- **Isolamento**: processos isolados do host
- **Portabilidade**: "funciona na minha máquina" = funciona em produção
- **Eficiência**: mais leve que VMs

**Docker Compose**: orquestra múltiplos containers localmente

---

## 3. ARQUITETURA DA SOLUÇÃO

### 3.1 Visão Geral

[INSERIR DIAGRAMA DE ARQUITETURA AQUI]

```
┌─────────────┐
│   Cliente   │
└──────┬──────┘
       │
┌──────▼───────┐
│ API Gateway  │ (Nginx - Opcional)
└──────┬───────┘
       │
   ┌───┴───┬───────────┬──────────┐
   │       │           │          │
┌──▼──┐ ┌─▼──┐  ┌─────▼────┐ ┌───▼────┐
│Cata │ │Carr│  │ Catálogo │ │Pedidos │
│logo │ │inho│  │ Réplica  │ │        │
└──┬──┘ └─┬──┘  └────┬─────┘ └───┬────┘
   │      │          │            │
┌──▼──┐ ┌▼──┐  ┌────▼─────┐ ┌───▼────┐
│PG DB│ │Redis│ │ PG Repl  │ │ PG DB  │
└─────┘ └─────┘ └──────────┘ └────────┘
```

### 3.2 Decomposição em Microserviços

#### 3.2.1 Critérios de Decomposição

Utilizou-se decomposição por **capacidade de negócio**:
- **Catálogo**: gerencia produtos e categorias
- **Carrinho**: gerencia sessões e itens
- **Pedidos**: gerencia finalização e histórico

#### 3.2.2 Bounded Contexts (DDD)

Cada serviço possui seu próprio modelo de domínio:
- Catálogo: `Produto`, `Categoria`, `Estoque`
- Carrinho: `Sessão`, `ItemCarrinho`
- Pedidos: `Pedido`, `ItemPedido`, `StatusPedido`

### 3.3 Decisões de Design

#### 3.3.1 Banco de Dados por Serviço

**Decisão**: Cada microserviço possui banco de dados próprio

**Justificativa**:
- ✅ Baixo acoplamento
- ✅ Escalabilidade independente
- ✅ Tecnologias heterogêneas (PostgreSQL + Redis)

**Trade-off**: 
- ❌ Transações distribuídas complexas
- ❌ Joins entre serviços impossíveis

#### 3.3.2 Comunicação Síncrona (REST)

**Decisão**: APIs REST para comunicação inter-serviços

**Justificativa**:
- ✅ Simplicidade de implementação
- ✅ Debuggabilidade
- ✅ Familiaridade da equipe

**Alternativa considerada**: RabbitMQ (assíncrona)
- ⚠️ Maior complexidade
- ⚠️ Overhead de infraestrutura

#### 3.3.3 Replicação Master-Slave

**Decisão**: PostgreSQL com replicação streaming

**Justificativa**:
- ✅ Alta disponibilidade para leituras
- ✅ Failover automático
- ✅ Suportado nativamente

### 3.4 Tecnologias Utilizadas

| Componente | Tecnologia | Versão | Justificativa |
|------------|-----------|--------|---------------|
| Backend | Python | 3.11 | Produtividade, ecossistema |
| Framework | Flask | 3.0 | Leve, RESTful |
| ORM | SQLAlchemy | 3.1 | Abstração de BD |
| BD Relacional | PostgreSQL | 15 | ACID, replicação |
| Cache/Sessão | Redis | 7 | Performance, TTL |
| Containers | Docker | 24.x | Portabilidade |
| Orquestração | Docker Compose | 2.x | Simplicidade local |

---

## 4. IMPLEMENTAÇÃO

### 4.1 Serviço de Catálogo

#### 4.1.1 Modelo de Dados

```python
class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), unique=True)
    
class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    preco = db.Column(db.Float)
    estoque = db.Column(db.Integer)
    categoria_id = db.Column(db.ForeignKey('categorias.id'))
```

#### 4.1.2 Endpoints Principais

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/produtos` | Lista produtos com filtros |
| GET | `/api/produtos/{id}` | Detalhes do produto |
| PUT | `/api/produtos/{id}/estoque` | Atualiza estoque |
| GET | `/health` | Health check |

#### 4.1.3 Controle de Estoque

```python
@app.route('/api/produtos/<int:id>/estoque', methods=['PUT'])
def atualizar_estoque(id):
    produto = Produto.query.get_or_404(id)
    operacao = request.json.get('operacao')
    quantidade = request.json.get('quantidade')
    
    if operacao == 'remover':
        if produto.estoque < quantidade:
            return jsonify({'error': 'Estoque insuficiente'}), 400
        produto.estoque -= quantidade
    
    db.session.commit()
    return jsonify(produto.to_dict()), 200
```

### 4.2 Serviço de Carrinho

#### 4.2.1 Armazenamento em Redis

```python
def salvar_carrinho(session_id, carrinho):
    redis_client.setex(
        f'carrinho:{session_id}',
        CARRINHO_TTL,  # 24 horas
        json.dumps(carrinho)
    )
```

#### 4.2.2 Validação com Catálogo

```python
def validar_produto_catalogo(produto_id, quantidade):
    response = requests.get(
        f'{CATALOGO_URL}/api/produtos/{produto_id}/estoque',
        params={'quantidade': quantidade}
    )
    return response.json()['data']['disponivel']
```

### 4.3 Replicação PostgreSQL

#### 4.3.1 Configuração

**postgresql.conf (Master)**:
```
wal_level = replica
max_wal_senders = 3
wal_keep_size = 64
```

**recovery.conf (Slave)**:
```
primary_conninfo = 'host=catalogo-db port=5432 user=replicator'
hot_standby = on
```

#### 4.3.2 Verificação de Status

```sql
-- No master
SELECT * FROM pg_stat_replication;

-- No slave
SELECT pg_is_in_recovery();
```

### 4.4 Containerização

#### 4.4.1 Dockerfile (Catálogo)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "app:app"]
```

#### 4.4.2 Docker Compose

```yaml
services:
  catalogo-service:
    build: ./microservices/catalogo
    ports:
      - "5001:5001"
    depends_on:
      - catalogo-db
```

---

## 5. TESTES E RESULTADOS

### 5.1 Metodologia de Testes

#### 5.1.1 Ambiente de Testes

- **Hardware**: [PREENCHER - ex: i7-10th, 16GB RAM]
- **Sistema Operacional**: Windows 11
- **Docker**: 24.x
- **Ferramentas**: Apache Bench, cURL, Postman

#### 5.1.2 Métricas Avaliadas

1. **Latência**: tempo de resposta (ms)
2. **Throughput**: requisições por segundo
3. **Taxa de sucesso**: % requisições bem-sucedidas
4. **Tempo de recuperação**: tempo de failover (s)

### 5.2 Teste de Funcionalidade

[PREENCHER COM RESULTADOS]

**Objetivo**: Validar fluxo completo de compra

**Cenário**:
1. Listar produtos
2. Adicionar ao carrinho
3. Atualizar quantidade
4. Finalizar pedido

**Resultado**: ✅ Todos os passos executados com sucesso

### 5.3 Teste de Concorrência

[PREENCHER COM RESULTADOS]

**Configuração**: 100 usuários simultâneos, 1000 requisições

```bash
ab -n 1000 -c 100 http://localhost:5001/api/produtos
```

**Resultados**:

| Métrica | Valor |
|---------|-------|
| Tempo total | [X] segundos |
| Req/segundo | [X] |
| Latência média | [X] ms |
| Taxa de sucesso | [X]% |

**Gráfico**: [INSERIR GRÁFICO DE LATÊNCIA]

### 5.4 Teste de Tolerância a Falhas

[PREENCHER COM RESULTADOS]

**Cenário**: Simular queda do serviço primário de Catálogo

**Procedimento**:
1. Executar requisições contínuas
2. Parar container `catalogo-service`
3. Medir tempo até réplica assumir
4. Verificar perda de dados

**Resultados**:

| Métrica | Valor |
|---------|-------|
| Tempo de detecção | [X] segundos |
| Tempo de failover | [X] segundos |
| Requisições perdidas | [X] |
| Downtime total | [X] segundos |

**Conclusão**: [ANÁLISE]

### 5.5 Teste de Escalabilidade

[PREENCHER COM RESULTADOS]

**Cenário**: Escalar Carrinho para 3 instâncias

```bash
docker-compose up -d --scale carrinho-service=3
```

**Resultados**:

| Instâncias | Throughput (req/s) | Latência (ms) |
|------------|-------------------|---------------|
| 1 | [X] | [X] |
| 2 | [X] | [X] |
| 3 | [X] | [X] |

**Análise**: [DISCUTIR GANHO DE PERFORMANCE]

---

## 6. DISCUSSÃO

### 6.1 Desafios Encontrados

[PREENCHER]

1. **Consistência de estoque**: 
   - Problema: race condition em vendas simultâneas
   - Solução: locks otimistas no PostgreSQL

2. **Sincronização de réplica**:
   - Problema: delay de replicação (lag)
   - Solução: monitorar `pg_stat_replication`

3. **Gerenciamento de sessões**:
   - Problema: expiração de carrinhos
   - Solução: TTL no Redis

### 6.2 Conceitos de Sistemas Distribuídos Aplicados

| Conceito | Aplicação | Evidência |
|----------|-----------|-----------|
| Transparência | API Gateway | Cliente não sabe quantos serviços existem |
| Replicação | PostgreSQL Replica | 2 instâncias do Catálogo |
| Particionamento | Serviços independentes | Cada serviço em container próprio |
| Concorrência | Redis | Múltiplas sessões simultâneas |
| Tolerância a falhas | Failover | Réplica assume quando primário cai |

### 6.3 Trade-offs

#### CAP Theorem
- **Escolha**: CP (Consistency + Partition tolerance)
- **Justificativa**: E-commerce requer consistência de estoque
- **Sacrifício**: Disponibilidade (sistema pode ficar indisponível durante partições)

#### Microserviços vs Monolito
- **Ganhos**: Escalabilidade, deploy independente
- **Custos**: Complexidade operacional, latência de rede

---

## 7. CONCLUSÃO

### 7.1 Objetivos Alcançados

✅ Implementação de marketplace distribuído com 2+ microserviços  
✅ Comunicação REST entre serviços  
✅ Replicação de banco de dados  
✅ Testes de concorrência, falhas e escalabilidade  
✅ Documentação completa  

### 7.2 Contribuições

Este trabalho contribuiu para:
1. Compreensão prática de sistemas distribuídos
2. Experiência com arquitetura de microserviços
3. Domínio de tecnologias de containerização
4. Análise de trade-offs em sistemas reais

### 7.3 Limitações

- Replicação apenas do Catálogo (Pedidos não replicado)
- Comunicação síncrona (não explora mensageria)
- Testes em ambiente local (não em nuvem)

### 7.4 Trabalhos Futuros

1. **Mensageria Assíncrona**: Implementar RabbitMQ para eventos
2. **Service Mesh**: Istio para observabilidade
3. **Deploy Kubernetes**: Orquestração em produção
4. **CQRS**: Separar leituras e escritas
5. **Event Sourcing**: Log imutável de eventos
6. **API Gateway**: Kong com autenticação JWT
7. **Monitoramento**: Prometheus + Grafana

---

## REFERÊNCIAS

BREWER, E. A. **CAP Twelve Years Later: How the "Rules" Have Changed**. IEEE Computer, v. 45, n. 2, p. 23-29, 2012.

COULOURIS, G. et al. **Distributed Systems: Concepts and Design**. 5th ed. Addison-Wesley, 2013.

FOWLER, M. **Microservices**. martinfowler.com, 2014. Disponível em: https://martinfowler.com/articles/microservices.html

KLEPPMANN, M. **Designing Data-Intensive Applications**. O'Reilly Media, 2017.

NEWMAN, S. **Building Microservices: Designing Fine-Grained Systems**. O'Reilly Media, 2015.

TANENBAUM, A. S.; VAN STEEN, M. **Distributed Systems: Principles and Paradigms**. 3rd ed. Pearson, 2017.

---

## ANEXOS

### Anexo A: Código-Fonte Completo
[Link para repositório GitHub]

### Anexo B: Diagramas de Sequência
[INSERIR DIAGRAMAS]

### Anexo C: Configurações de Infraestrutura
[docker-compose.yml, Dockerfiles, etc.]

### Anexo D: Scripts de Teste
[Scripts de Apache Bench, Locust, etc.]

---

**Páginas**: [PREENCHER]  
**Palavras**: [PREENCHER]  
**Data de Submissão**: [PREENCHER]
