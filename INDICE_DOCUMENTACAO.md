# 📚 Índice de Documentação - Sistema Distribuído de Confeitaria

## 🎯 Comece por Aqui

Se você é novo no projeto, leia os documentos nesta ordem:

1. **`RESUMO_EXECUTIVO.md`** ⭐ - **LEIA PRIMEIRO!**
   - Visão geral de como o projeto se enquadra no TCC
   - Checklist de requisitos atendidos
   - Próximos passos imediatos

2. **`README.md`**
   - Introdução ao projeto
   - Quick start
   - APIs documentadas

3. **`ARQUITETURA_DISTRIBUIDA.md`**
   - Design completo do sistema
   - Conceitos de sistemas distribuídos aplicados
   - Diferenciais do projeto

4. **`GUIA_EXECUCAO.md`**
   - Como rodar o sistema passo a passo
   - Testes práticos
   - Troubleshooting

5. **`PLANO_IMPLEMENTACAO.md`**
   - Cronograma de 8 semanas
   - Tarefas detalhadas semana a semana
   - Checkpoints de validação

---

## 📖 Documentos Principais

### 1. RESUMO_EXECUTIVO.md
**O que é**: Documento executivo que explica como seu projeto atende ao TCC  
**Quando usar**: Primeira leitura, para entender o contexto geral  
**Conteúdo**:
- ✅ Situação atual vs objetivo
- ✅ Estratégia de decomposição
- ✅ Checklist de requisitos atendidos
- ✅ Diferenciais do projeto
- ✅ Cronograma sugerido
- ✅ Próximos passos imediatos

---

### 2. README.md
**O que é**: Documentação oficial do projeto (formato GitHub)  
**Quando usar**: Para entender funcionalidades e APIs  
**Conteúdo**:
- ✅ Descrição do projeto
- ✅ Arquitetura visual
- ✅ Instalação e quick start
- ✅ Testes práticos
- ✅ APIs documentadas
- ✅ Stack tecnológico

---

### 3. ARQUITETURA_DISTRIBUIDA.md
**O que é**: Documento técnico detalhado da arquitetura  
**Quando usar**: Para estudo aprofundado e relatório do TCC  
**Conteúdo**:
- ✅ Visão geral do projeto
- ✅ Arquitetura com diagramas
- ✅ Decomposição em microserviços (3 serviços)
- ✅ Conceitos de SD aplicados (transparência, replicação, etc.)
- ✅ Tecnologias utilizadas e justificativas
- ✅ Plano de implementação de 8 semanas
- ✅ Diferenciais para nota máxima
- ✅ Requisitos técnicos atendidos

---

### 4. GUIA_EXECUCAO.md
**O que é**: Manual prático de como executar o sistema  
**Quando usar**: Durante implementação e testes  
**Conteúdo**:
- ✅ Pré-requisitos
- ✅ Início rápido (comandos Docker)
- ✅ Como popular banco de dados
- ✅ Testes dos microserviços (cURL, PowerShell)
- ✅ Comandos Docker úteis
- ✅ Testes de tolerância a falhas
- ✅ Testes de escalabilidade
- ✅ Ferramentas de administração (pgAdmin, Redis Commander)
- ✅ Troubleshooting

---

### 5. PLANO_IMPLEMENTACAO.md
**O que é**: Cronograma detalhado de 8 semanas  
**Quando usar**: Como guia de implementação passo a passo  
**Conteúdo**:
- ✅ Semana 1: Preparação e setup
- ✅ Semana 2: Serviço de Catálogo
- ✅ Semana 3: Replicação do Catálogo
- ✅ Semana 4: Serviço de Carrinho
- ✅ Semana 5: Integração e Frontend
- ✅ Semana 6: Deploy e Infraestrutura
- ✅ Semana 7: Testes e Validação
- ✅ Semana 8: Documentação e Apresentação
- ✅ Checklist final
- ✅ Próxima ação imediata

---

### 6. COMANDOS_UTEIS.md
**O que é**: Referência rápida de comandos  
**Quando usar**: Durante desenvolvimento e testes  
**Conteúdo**:
- ✅ Comandos Docker e Docker Compose
- ✅ Comandos PostgreSQL (SQL)
- ✅ Comandos Redis
- ✅ Testes com cURL
- ✅ Testes com PowerShell (Invoke-RestMethod)
- ✅ Testes de performance (Apache Bench)
- ✅ Scripts de teste de falha
- ✅ Python - ambiente virtual
- ✅ Monitoramento e debug
- ✅ Troubleshooting
- ✅ Comandos Git
- ✅ Exports e backups
- ✅ Comandos para apresentação do TCC

---

### 7. docs/RELATORIO_TEMPLATE.md
**O que é**: Template completo do relatório técnico (R.A.)  
**Quando usar**: Para escrever o relatório final do TCC  
**Conteúdo**:
- ✅ Resumo
- ✅ 1. Introdução (contexto, motivação, objetivos)
- ✅ 2. Fundamentação Teórica (SD, microserviços, REST, replicação)
- ✅ 3. Arquitetura da Solução (decomposição, decisões de design)
- ✅ 4. Implementação (código, replicação, Docker)
- ✅ 5. Testes e Resultados (funcionalidade, concorrência, falhas)
- ✅ 6. Discussão (desafios, trade-offs)
- ✅ 7. Conclusão (objetivos, limitações, trabalhos futuros)
- ✅ Referências bibliográficas
- ✅ Anexos

---

## 🔧 Arquivos de Código

### 8. microservices/catalogo/app.py
**O que é**: Implementação do microserviço de Catálogo  
**Funcionalidades**:
- ✅ 8 endpoints REST
- ✅ Gerenciamento de produtos e categorias
- ✅ Controle de estoque
- ✅ Health check
- ✅ Integração com PostgreSQL

**Endpoints principais**:
- `GET /api/produtos` - Listar produtos
- `GET /api/produtos/{id}` - Detalhes do produto
- `PUT /api/produtos/{id}/estoque` - Atualizar estoque
- `GET /api/categorias` - Listar categorias
- `GET /health` - Health check

---

### 9. microservices/carrinho/app.py
**O que é**: Implementação do microserviço de Carrinho  
**Funcionalidades**:
- ✅ Gerenciamento de sessões com Redis
- ✅ Comunicação REST com Catálogo
- ✅ TTL automático (24h)
- ✅ Validação de estoque

**Endpoints principais**:
- `POST /api/carrinho/sessao` - Criar sessão
- `POST /api/carrinho/{id}/adicionar` - Adicionar item
- `GET /api/carrinho/{id}` - Obter carrinho
- `DELETE /api/carrinho/{id}/remover/{produto_id}` - Remover item
- `DELETE /api/carrinho/{id}` - Limpar carrinho
- `GET /health` - Health check

---

### 10. docker-compose.yml
**O que é**: Orquestração de todos os serviços  
**Serviços incluídos**:
- ✅ catalogo-db (PostgreSQL master)
- ✅ catalogo-db-replica (PostgreSQL slave)
- ✅ redis (cache/sessões)
- ✅ pedidos-db (PostgreSQL)
- ✅ catalogo-service (Flask)
- ✅ catalogo-service-replica (Flask)
- ✅ carrinho-service (Flask)
- ✅ pgAdmin (ferramenta admin - opcional)
- ✅ redis-commander (ferramenta admin - opcional)

---

### 11. microservices/catalogo/seed_data.py
**O que é**: Script para popular banco com dados de teste  
**Como usar**:
```powershell
docker exec -it catalogo-service python seed_data.py
```
**Dados criados**:
- 5 categorias
- 13 produtos de exemplo
- Estoque variado

---

### 12. microservices/catalogo/Dockerfile
**O que é**: Imagem Docker do serviço de Catálogo  
**Base**: Python 3.11-slim  
**Porta**: 5001  
**Servidor**: Gunicorn (4 workers)

---

### 13. microservices/carrinho/Dockerfile
**O que é**: Imagem Docker do serviço de Carrinho  
**Base**: Python 3.11-slim  
**Porta**: 5002  
**Servidor**: Gunicorn (4 workers)

---

## 📁 Outros Arquivos Importantes

### 14. .gitignore
**O que é**: Arquivos ignorados pelo Git  
**Ignora**:
- Ambientes virtuais (`venv/`)
- Cache Python (`__pycache__/`)
- Variáveis de ambiente (`.env`)
- Bancos SQLite (`*.sqlite3`)
- Volumes Docker
- Logs

---

### 15. microservices/catalogo/.env.example
**O que é**: Exemplo de variáveis de ambiente do Catálogo  
**Como usar**: Copiar para `.env` e ajustar valores

---

### 16. microservices/carrinho/.env.example
**O que é**: Exemplo de variáveis de ambiente do Carrinho  
**Como usar**: Copiar para `.env` e ajustar valores

---

## 🗂️ Estrutura Completa de Pastas

```
confeitaria-main/
│
├── 📄 RESUMO_EXECUTIVO.md          ⭐ LEIA PRIMEIRO!
├── 📄 README.md                     Documentação principal
├── 📄 ARQUITETURA_DISTRIBUIDA.md    Design detalhado
├── 📄 GUIA_EXECUCAO.md              Manual de execução
├── 📄 PLANO_IMPLEMENTACAO.md        Cronograma 8 semanas
├── 📄 COMANDOS_UTEIS.md             Referência rápida
├── 📄 INDICE_DOCUMENTACAO.md        Este arquivo
├── 📄 .gitignore                    Git ignore
├── 📄 docker-compose.yml            Orquestração
│
├── 📁 docs/
│   └── 📄 RELATORIO_TEMPLATE.md     Template do relatório TCC
│
├── 📁 microservices/
│   │
│   ├── 📁 catalogo/
│   │   ├── 📄 app.py                Código do serviço
│   │   ├── 📄 Dockerfile            Imagem Docker
│   │   ├── 📄 requirements.txt      Dependências Python
│   │   ├── 📄 seed_data.py          Popular banco
│   │   └── 📄 .env.example          Exemplo de config
│   │
│   ├── 📁 carrinho/
│   │   ├── 📄 app.py                Código do serviço
│   │   ├── 📄 Dockerfile            Imagem Docker
│   │   ├── 📄 requirements.txt      Dependências Python
│   │   └── 📄 .env.example          Exemplo de config
│   │
│   └── 📁 pedidos/                  (Opcional - bônus)
│       ├── 📄 app.py
│       ├── 📄 Dockerfile
│       └── 📄 requirements.txt
│
├── 📁 confeitaria/                  (Django original - monolito)
│   ├── models.py
│   ├── views.py
│   └── ...
│
├── 📁 pedidos/                      (Django original - monolito)
│   ├── models.py
│   ├── views.py
│   └── ...
│
└── 📁 setup/                        (Django original - monolito)
    ├── settings.py
    └── ...
```

---

## 🎯 Fluxo de Uso dos Documentos

### Para Começar (Dia 1)
1. **RESUMO_EXECUTIVO.md** - Entender contexto
2. **README.md** - Visão geral
3. **GUIA_EXECUCAO.md** - Rodar pela primeira vez

### Durante Implementação (Semanas 1-6)
1. **PLANO_IMPLEMENTACAO.md** - Seguir cronograma
2. **ARQUITETURA_DISTRIBUIDA.md** - Consultar design
3. **COMANDOS_UTEIS.md** - Referência rápida
4. **GUIA_EXECUCAO.md** - Testes

### Durante Testes (Semana 7)
1. **GUIA_EXECUCAO.md** - Testes funcionais
2. **COMANDOS_UTEIS.md** - Testes de carga
3. **PLANO_IMPLEMENTACAO.md** - Checklist de testes

### Escrevendo Relatório (Semana 8)
1. **docs/RELATORIO_TEMPLATE.md** - Estrutura
2. **ARQUITETURA_DISTRIBUIDA.md** - Conteúdo técnico
3. **README.md** - Resumo das tecnologias

### Preparando Apresentação (Semana 8)
1. **RESUMO_EXECUTIVO.md** - Slides principais
2. **COMANDOS_UTEIS.md** - Demo ao vivo
3. **ARQUITETURA_DISTRIBUIDA.md** - Diagramas

---

## 📊 Mapa Mental dos Documentos

```
RESUMO_EXECUTIVO.md (START HERE!)
    │
    ├─► README.md
    │       │
    │       ├─► ARQUITETURA_DISTRIBUIDA.md
    │       │       │
    │       │       └─► docs/RELATORIO_TEMPLATE.md
    │       │
    │       └─► GUIA_EXECUCAO.md
    │               │
    │               └─► COMANDOS_UTEIS.md
    │
    └─► PLANO_IMPLEMENTACAO.md
            │
            ├─► Semana 1-8 (Cronograma)
            └─► Checkpoints
```

---

## 🔍 Busca Rápida por Tópico

| Preciso de... | Veja... |
|---------------|---------|
| Visão geral do projeto | `README.md` |
| Como começar | `RESUMO_EXECUTIVO.md` |
| Conceitos de SD | `ARQUITETURA_DISTRIBUIDA.md` |
| Rodar o sistema | `GUIA_EXECUCAO.md` |
| Cronograma | `PLANO_IMPLEMENTACAO.md` |
| Comandos Docker | `COMANDOS_UTEIS.md` |
| Escrever relatório | `docs/RELATORIO_TEMPLATE.md` |
| Testar APIs | `GUIA_EXECUCAO.md` ou `COMANDOS_UTEIS.md` |
| Resolver problemas | `GUIA_EXECUCAO.md` (seção Troubleshooting) |
| Popular banco | `microservices/catalogo/seed_data.py` |
| Configurar .env | `.env.example` |

---

## 📝 Checklist de Leitura

Marque os documentos conforme você os lê:

- [ ] RESUMO_EXECUTIVO.md
- [ ] README.md
- [ ] ARQUITETURA_DISTRIBUIDA.md
- [ ] GUIA_EXECUCAO.md
- [ ] PLANO_IMPLEMENTACAO.md
- [ ] COMANDOS_UTEIS.md
- [ ] docs/RELATORIO_TEMPLATE.md
- [ ] docker-compose.yml (revisão)
- [ ] microservices/catalogo/app.py (revisão)
- [ ] microservices/carrinho/app.py (revisão)

---

## ✅ Status da Documentação

| Documento | Status | Última Atualização |
|-----------|--------|-------------------|
| RESUMO_EXECUTIVO.md | ✅ Completo | 17 Out 2025 |
| README.md | ✅ Completo | 17 Out 2025 |
| ARQUITETURA_DISTRIBUIDA.md | ✅ Completo | 16 Out 2025 |
| GUIA_EXECUCAO.md | ✅ Completo | 16 Out 2025 |
| PLANO_IMPLEMENTACAO.md | ✅ Completo | 17 Out 2025 |
| COMANDOS_UTEIS.md | ✅ Completo | 17 Out 2025 |
| docs/RELATORIO_TEMPLATE.md | ✅ Completo | 17 Out 2025 |
| Código dos Microserviços | ✅ Completo | 16 Out 2025 |
| Docker Compose | ✅ Completo | 16 Out 2025 |

---

## 🎓 Recomendação de Leitura para o TCC

### Fase 1: Entendimento (1-2 horas)
1. RESUMO_EXECUTIVO.md (15 min)
2. README.md (20 min)
3. ARQUITETURA_DISTRIBUIDA.md (45 min)

### Fase 2: Prática (2-3 horas)
1. GUIA_EXECUCAO.md (30 min)
2. Executar sistema (1 hora)
3. Testar APIs (30 min)
4. COMANDOS_UTEIS.md (referência)

### Fase 3: Implementação (40+ horas)
1. PLANO_IMPLEMENTACAO.md (seguir semanas)
2. Código dos microserviços
3. Testes contínuos

### Fase 4: Documentação (8-10 horas)
1. docs/RELATORIO_TEMPLATE.md
2. Preencher com resultados
3. Revisar e finalizar

---

**Última atualização**: 17 de Outubro de 2025  
**Autor**: Paulo H.  
**Total de Documentos**: 16 arquivos principais

---

## 💡 Dica Final

**Imprima esta página** ou mantenha-a aberta como referência enquanto trabalha no projeto. Sempre que estiver perdido, volte aqui para saber qual documento consultar!

**Boa sorte no TCC!** 🚀
