# Plano de Implementação - TCC Sistema Distribuído

## 📅 CRONOGRAMA DETALHADO (8 SEMANAS)

---

## SEMANA 1: Preparação e Setup (17-23 Out 2025)

### Objetivos
- [ ] Configurar ambiente de desenvolvimento
- [ ] Estruturar repositório Git
- [ ] Instalar ferramentas necessárias
- [ ] Estudar conceitos teóricos

### Tarefas Técnicas

#### Dia 1-2: Ambiente
```powershell
# Instalar Docker Desktop
# Verificar instalação
docker --version
docker-compose --version

# Criar estrutura de pastas
cd "C:\Users\PauloH\Documents\trabalho confeitaria\confeitaria-main"
mkdir microservices\catalogo
mkdir microservices\carrinho
mkdir microservices\pedidos
mkdir docs
mkdir tests
```

#### Dia 3-4: Git e Documentação
```powershell
# Inicializar repositório (se ainda não foi)
git init
git add .
git commit -m "Initial commit - Monolith version"

# Criar branch para microserviços
git checkout -b feature/microservices

# Adicionar arquivos já criados
git add ARQUITETURA_DISTRIBUIDA.md
git add GUIA_EXECUCAO.md
git add docker-compose.yml
git add microservices/
git commit -m "Add microservices architecture documentation"
```

#### Dia 5-7: Estudo Teórico
- [ ] Ler sobre Sistemas Distribuídos (CAP Theorem)
- [ ] Estudar REST APIs (HTTP Methods, Status Codes)
- [ ] Revisar Docker e containers
- [ ] Entender Redis e PostgreSQL

### Entregável Semana 1
✅ Ambiente configurado  
✅ Repositório Git estruturado  
✅ Documentação inicial pronta  

---

## SEMANA 2: Serviço de Catálogo (24-30 Out 2025)

### Objetivos
- [ ] Implementar API REST do Catálogo
- [ ] Configurar PostgreSQL
- [ ] Criar Dockerfile e testar
- [ ] Migrar dados do Django

### Tarefas

#### Passo 1: Criar e Testar Localmente
```powershell
# Navegar para pasta do serviço
cd microservices\catalogo

# Criar ambiente virtual Python
python -m venv venv
.\venv\Scripts\Activate.ps1

# Instalar dependências
pip install -r requirements.txt

# Criar arquivo .env
New-Item -Path .env -ItemType File
```

**Conteúdo do .env:**
```env
DATABASE_URL=postgresql://catalogo_user:catalogo_pass@localhost:5432/catalogo_db
PORT=5001
DEBUG=True
```

#### Passo 2: Iniciar PostgreSQL Local
```powershell
# Via Docker
docker run -d --name catalogo-db-local `
  -e POSTGRES_DB=catalogo_db `
  -e POSTGRES_USER=catalogo_user `
  -e POSTGRES_PASSWORD=catalogo_pass `
  -p 5432:5432 `
  postgres:15-alpine
```

#### Passo 3: Executar e Testar
```powershell
# Iniciar aplicação
python app.py

# Em outro terminal, testar
curl http://localhost:5001/health
curl http://localhost:5001/api/categorias
```

#### Passo 4: Migrar Dados do Django
```python
# Script: migrate_data.py
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from confeitaria.models import Doce, Categoria as DjangoCategoria
import requests

# Migrar categorias
categorias_django = DjangoCategoria.objects.all()
for cat in categorias_django:
    response = requests.post('http://localhost:5001/api/categorias', json={
        'nome': cat.nome
    })
    print(f"Categoria {cat.nome}: {response.status_code}")

# Migrar produtos
doces_django = Doce.objects.all()
for doce in doces_django:
    response = requests.post('http://localhost:5001/api/produtos', json={
        'nome': doce.nome,
        'descricao': doce.descricao,
        'preco': doce.preco,
        'estoque': doce.estoque,
        'categoria_id': doce.categoria.id
    })
    print(f"Produto {doce.nome}: {response.status_code}")
```

#### Passo 5: Dockerizar
```powershell
# Build da imagem
docker build -t catalogo-service:v1 .

# Testar container
docker run -d -p 5001:5001 `
  -e DATABASE_URL=postgresql://catalogo_user:catalogo_pass@host.docker.internal:5432/catalogo_db `
  --name catalogo-test `
  catalogo-service:v1

# Verificar logs
docker logs -f catalogo-test
```

### Entregável Semana 2
✅ Serviço de Catálogo funcional  
✅ API REST com 5+ endpoints  
✅ Dockerfile pronto  
✅ Dados migrados  

---

## SEMANA 3: Replicação do Catálogo (31 Out - 6 Nov 2025)

### Objetivos
- [ ] Configurar PostgreSQL Replication
- [ ] Implementar Load Balancing
- [ ] Testar failover
- [ ] Documentar processo

### Tarefas

#### Passo 1: Configurar Replicação PostgreSQL

**Arquivo: `setup_replication.sql`**
```sql
-- No servidor PRIMÁRIO
-- Criar usuário de replicação
CREATE ROLE replicator WITH REPLICATION LOGIN PASSWORD 'repl_pass';

-- Configurar pg_hba.conf
-- host replication replicator <ip_replica> md5

-- Configurar postgresql.conf
-- wal_level = replica
-- max_wal_senders = 3
```

#### Passo 2: Docker Compose com Réplica
```powershell
# Usar docker-compose.yml já criado
docker-compose up -d catalogo-db catalogo-db-replica

# Verificar sincronização
docker exec -it catalogo-db psql -U catalogo_user -d catalogo_db -c "SELECT * FROM pg_stat_replication;"
```

#### Passo 3: Configurar Nginx (Load Balancer)

**Arquivo: `nginx.conf`**
```nginx
upstream catalogo_backend {
    server catalogo-service:5001;
    server catalogo-service-replica:5001;
}

server {
    listen 80;
    
    location /api/produtos {
        proxy_pass http://catalogo_backend;
        proxy_set_header Host $host;
    }
}
```

#### Passo 4: Testes de Failover
```powershell
# Teste 1: Parar primário
docker-compose stop catalogo-service

# Teste 2: Requisições devem continuar funcionando via réplica
for ($i=1; $i -le 10; $i++) {
    curl http://localhost:5011/api/produtos
    Start-Sleep -Seconds 1
}

# Teste 3: Reiniciar primário
docker-compose start catalogo-service
```

### Entregável Semana 3
✅ Replicação PostgreSQL funcionando  
✅ Load Balancer configurado  
✅ Testes de failover documentados  

---

## SEMANA 4: Serviço de Carrinho (7-13 Nov 2025)

### Objetivos
- [ ] Implementar API do Carrinho
- [ ] Integrar com Redis
- [ ] Comunicação com Catálogo
- [ ] Testar sessões

### Tarefas

#### Passo 1: Setup Redis
```powershell
# Iniciar Redis
docker run -d --name redis-local -p 6379:6379 redis:7-alpine

# Testar conexão
docker exec -it redis-local redis-cli ping
```

#### Passo 2: Desenvolver Serviço
```powershell
cd microservices\carrinho

# Criar ambiente virtual
python -m venv venv
.\venv\Scripts\Activate.ps1

# Instalar dependências
pip install -r requirements.txt

# Executar
python app.py
```

#### Passo 3: Testar Integração
```powershell
# 1. Criar sessão
$session = Invoke-RestMethod -Uri "http://localhost:5002/api/carrinho/sessao" -Method POST
$sid = $session.data.session_id

# 2. Adicionar item (comunicação com Catálogo)
$body = @{produto_id=1; quantidade=2} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:5002/api/carrinho/$sid/adicionar" `
    -Method POST -ContentType "application/json" -Body $body

# 3. Ver carrinho
Invoke-RestMethod -Uri "http://localhost:5002/api/carrinho/$sid" -Method GET
```

#### Passo 4: Testar Persistência
```powershell
# Reiniciar serviço
docker-compose restart carrinho-service

# Verificar se dados persistem no Redis
Invoke-RestMethod -Uri "http://localhost:5002/api/carrinho/$sid" -Method GET
```

### Entregável Semana 4
✅ Serviço de Carrinho funcional  
✅ Integração com Redis  
✅ Comunicação REST com Catálogo  
✅ Sessões persistentes  

---

## SEMANA 5: Integração e Frontend (14-20 Nov 2025)

### Objetivos
- [ ] Adaptar frontend Django para APIs
- [ ] Implementar API Gateway
- [ ] Testar fluxo completo
- [ ] Resolver bugs

### Tarefas

#### Passo 1: Criar Cliente HTTP no Django

**Arquivo: `confeitaria/api_client.py`**
```python
import requests
from django.conf import settings

class CatalogoClient:
    BASE_URL = 'http://localhost:5001'
    
    @staticmethod
    def listar_produtos(categoria_id=None):
        params = {'categoria_id': categoria_id} if categoria_id else {}
        response = requests.get(f'{CatalogoClient.BASE_URL}/api/produtos', params=params)
        return response.json()['data']
    
    @staticmethod
    def obter_produto(produto_id):
        response = requests.get(f'{CatalogoClient.BASE_URL}/api/produtos/{produto_id}')
        return response.json()['data']

class CarrinhoClient:
    BASE_URL = 'http://localhost:5002'
    
    @staticmethod
    def obter_carrinho(session_id):
        response = requests.get(f'{CarrinhoClient.BASE_URL}/api/carrinho/{session_id}')
        return response.json()['data']
    
    @staticmethod
    def adicionar_item(session_id, produto_id, quantidade):
        response = requests.post(
            f'{CarrinhoClient.BASE_URL}/api/carrinho/{session_id}/adicionar',
            json={'produto_id': produto_id, 'quantidade': quantidade}
        )
        return response.json()
```

#### Passo 2: Adaptar Views Django
```python
# confeitaria/views.py
from confeitaria.api_client import CatalogoClient, CarrinhoClient

def index(request):
    # Buscar produtos da API
    produtos = CatalogoClient.listar_produtos()
    categorias = CatalogoClient.listar_categorias()
    
    return render(request, 'confeitaria/index.html', {
        'doces': produtos,
        'categorias': categorias
    })
```

#### Passo 3: Configurar API Gateway (Nginx)

**Arquivo: `nginx/nginx.conf`**
```nginx
server {
    listen 80;
    
    # Frontend Django
    location / {
        proxy_pass http://frontend:8000;
    }
    
    # API Catálogo
    location /api/catalogo/ {
        rewrite ^/api/catalogo/(.*) /api/$1 break;
        proxy_pass http://catalogo-service:5001;
    }
    
    # API Carrinho
    location /api/carrinho/ {
        rewrite ^/api/carrinho/(.*) /api/carrinho/$1 break;
        proxy_pass http://carrinho-service:5002;
    }
}
```

### Entregável Semana 5
✅ Frontend integrado com APIs  
✅ API Gateway configurado  
✅ Fluxo completo funcionando  

---

## SEMANA 6: Deploy e Infraestrutura (21-27 Nov 2025)

### Objetivos
- [ ] Deploy completo com Docker Compose
- [ ] Configurar monitoramento
- [ ] Otimizar performance
- [ ] Deploy em nuvem (opcional)

### Tarefas

#### Passo 1: Subir Stack Completa
```powershell
# Subir todos os serviços
docker-compose up -d

# Verificar saúde
docker-compose ps
docker-compose logs -f
```

#### Passo 2: Configurar Monitoramento (Opcional)

**Prometheus + Grafana**
```yaml
# Adicionar ao docker-compose.yml
prometheus:
  image: prom/prometheus
  volumes:
    - ./prometheus.yml:/etc/prometheus/prometheus.yml
  ports:
    - "9090:9090"

grafana:
  image: grafana/grafana
  ports:
    - "3000:3000"
```

#### Passo 3: Deploy na Nuvem (Opcional)

**AWS ECS / Google Cloud Run / Azure Container Instances**
```powershell
# Exemplo AWS
aws ecr create-repository --repository-name catalogo-service
docker tag catalogo-service:v1 <account>.dkr.ecr.<region>.amazonaws.com/catalogo-service:v1
docker push <account>.dkr.ecr.<region>.amazonaws.com/catalogo-service:v1
```

### Entregável Semana 6
✅ Sistema completo rodando  
✅ Monitoramento configurado  
✅ Deploy em produção (opcional)  

---

## SEMANA 7: Testes e Validação (28 Nov - 4 Dez 2025)

### Objetivos
- [ ] Testes de concorrência
- [ ] Testes de tolerância a falhas
- [ ] Testes de escalabilidade
- [ ] Coletar métricas

### Testes Obrigatórios

#### Teste 1: Concorrência (100 usuários)
```powershell
# Usando Apache Bench
docker run --rm --network=confeitaria-network jordi/ab `
  -n 1000 -c 100 http://catalogo-service:5001/api/produtos

# Coletar métricas:
# - Tempo médio de resposta
# - Taxa de sucesso
# - Throughput (req/s)
```

#### Teste 2: Tolerância a Falhas
```powershell
# Script de teste
for ($i=1; $i -le 5; $i++) {
    Write-Host "=== Rodada $i ==="
    
    # Fazer requisições
    curl http://localhost:5001/api/produtos
    
    # Derrubar serviço primário
    docker-compose stop catalogo-service
    Start-Sleep -Seconds 2
    
    # Verificar se réplica assume
    $response = curl http://localhost:5011/api/produtos
    Write-Host "Réplica respondeu: $($response.StatusCode)"
    
    # Reiniciar primário
    docker-compose start catalogo-service
    Start-Sleep -Seconds 5
}
```

#### Teste 3: Escalabilidade
```powershell
# Escalar carrinho para 3 instâncias
docker-compose up -d --scale carrinho-service=3

# Testar distribuição de carga
for ($i=1; $i -le 100; $i++) {
    curl http://localhost:5002/health
}
```

### Entregável Semana 7
✅ Relatório de testes  
✅ Gráficos de desempenho  
✅ Análise de resultados  

---

## SEMANA 8: Documentação e Apresentação (5-11 Dez 2025)

### Objetivos
- [ ] Escrever relatório técnico (R.A.)
- [ ] Criar apresentação
- [ ] Gravar demo em vídeo
- [ ] Revisar código

### Estrutura do Relatório

#### 1. Introdução (2-3 páginas)
- Contexto de sistemas distribuídos
- Conceitos teóricos (CAP, transparência, etc.)
- Objetivos do projeto

#### 2. Arquitetura (3-4 páginas)
- Diagrama da arquitetura
- Descrição dos microserviços
- Tecnologias escolhidas (justificativas)
- Padrões aplicados

#### 3. Implementação (4-5 páginas)
- Detalhes técnicos de cada serviço
- Comunicação REST
- Replicação e failover
- Gerenciamento de sessões

#### 4. Testes e Resultados (3-4 páginas)
- Metodologia de testes
- Resultados de concorrência
- Resultados de tolerância a falhas
- Resultados de escalabilidade
- Gráficos e tabelas

#### 5. Conclusão (1-2 páginas)
- Objetivos alcançados
- Desafios enfrentados
- Aprendizados
- Trabalhos futuros

#### 6. Referências
- Livros, artigos, documentação

### Apresentação (10-15 minutos)

**Slide 1**: Título e Introdução  
**Slide 2**: Problema e Objetivos  
**Slide 3**: Conceitos de Sistemas Distribuídos  
**Slide 4**: Arquitetura da Solução  
**Slide 5**: Microserviço de Catálogo  
**Slide 6**: Microserviço de Carrinho  
**Slide 7**: Replicação e Tolerância a Falhas  
**Slide 8**: Demo ao Vivo  
**Slide 9**: Resultados dos Testes  
**Slide 10**: Conclusão e Aprendizados  

### Entregável Semana 8
✅ Relatório técnico completo  
✅ Apresentação em slides  
✅ Vídeo de demonstração  
✅ Código no GitHub  

---

## 📊 CHECKLIST FINAL

### Requisitos Técnicos
- [ ] Mínimo 2 serviços implementados
- [ ] Serviços em nós independentes (containers)
- [ ] Comunicação REST entre serviços
- [ ] Suporte a múltiplos usuários
- [ ] Replicação de ao menos 1 serviço
- [ ] Relatório de tolerância a falhas

### Entregáveis
- [ ] Código-fonte no Git
- [ ] README.md detalhado
- [ ] Docker Compose funcional
- [ ] Relatório técnico (R.A.)
- [ ] Apresentação preparada

### Conceitos Aplicados
- [ ] Transparência de localização
- [ ] Transparência de replicação
- [ ] Escalabilidade horizontal
- [ ] Tolerância a falhas
- [ ] Concorrência
- [ ] Comunicação distribuída

---

## 🎯 PRÓXIMA AÇÃO IMEDIATA

**AGORA (Semana 1):**
```powershell
# 1. Verificar Docker instalado
docker --version

# 2. Testar serviço de catálogo localmente
cd microservices\catalogo
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py

# 3. Em outro terminal, testar
curl http://localhost:5001/health
```

**Começe por aqui e avance passo a passo!**

---

**Criado em**: 16 Out 2025  
**Prazo Final**: 11 Dez 2025 (8 semanas)  
**Autor**: Paulo H.
