# Guia de Execução - Sistema Distribuído de Confeitaria

## 📋 Pré-requisitos

- Docker Desktop instalado (Windows/Mac/Linux)
- Docker Compose instalado
- Git instalado
- 8GB RAM disponível (mínimo)
- Portas disponíveis: 5001, 5002, 5003, 5432, 5433, 5434, 6379, 8000, 5050, 8081

## 🚀 Início Rápido

### 1. Clonar o Repositório
```powershell
cd "C:\Users\PauloH\Documents\trabalho confeitaria\confeitaria-main"
```

### 2. Iniciar Todos os Serviços
```powershell
# Inicia todos os containers em modo detached
docker-compose up -d

# Verifica status dos containers
docker-compose ps
```

### 3. Verificar Logs
```powershell
# Logs de todos os serviços
docker-compose logs -f

# Logs de um serviço específico
docker-compose logs -f catalogo-service
docker-compose logs -f carrinho-service
```

### 4. Acessar os Serviços

| Serviço | URL | Descrição |
|---------|-----|-----------|
| **Catálogo API** | http://localhost:5001/api/produtos | API de produtos |
| **Catálogo Réplica** | http://localhost:5011/api/produtos | Réplica read-only |
| **Carrinho API** | http://localhost:5002/health | API de carrinho |
| **Health Checks** | http://localhost:5001/health | Status do catálogo |
| **pgAdmin** | http://localhost:5050 | Interface PostgreSQL |
| **Redis Commander** | http://localhost:8081 | Interface Redis |

## 🧪 Testando os Microserviços

### Testar Serviço de Catálogo

#### 1. Health Check
```powershell
curl http://localhost:5001/health
```

#### 2. Listar Produtos
```powershell
curl http://localhost:5001/api/produtos
```

#### 3. Listar Categorias
```powershell
curl http://localhost:5001/api/categorias
```

#### 4. Verificar Réplica
```powershell
# Réplica deve retornar os mesmos dados
curl http://localhost:5011/api/produtos
```

### Testar Serviço de Carrinho

#### 1. Criar Sessão
```powershell
$session = Invoke-RestMethod -Uri "http://localhost:5002/api/carrinho/sessao" -Method POST
$sessionId = $session.data.session_id
Write-Host "Session ID: $sessionId"
```

#### 2. Adicionar Item ao Carrinho
```powershell
$body = @{
    produto_id = 1
    quantidade = 2
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5002/api/carrinho/$sessionId/adicionar" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body
```

#### 3. Visualizar Carrinho
```powershell
Invoke-RestMethod -Uri "http://localhost:5002/api/carrinho/$sessionId" -Method GET
```

#### 4. Remover Item
```powershell
Invoke-RestMethod -Uri "http://localhost:5002/api/carrinho/$sessionId/remover/1" -Method DELETE
```

## 📊 Popular Banco de Dados (Dados de Teste)

### Criar Categorias e Produtos

```powershell
# Acesse o container do catálogo
docker exec -it catalogo-service bash

# Dentro do container, execute o Python
python3

# Cole o código abaixo:
from app import db, Categoria, Produto

# Cria as tabelas
db.create_all()

# Adiciona categorias
cat1 = Categoria(nome='Bolos')
cat2 = Categoria(nome='Doces Finos')
cat3 = Categoria(nome='Tortas')

db.session.add_all([cat1, cat2, cat3])
db.session.commit()

# Adiciona produtos
p1 = Produto(
    nome='Bolo de Chocolate',
    descricao='Delicioso bolo de chocolate com cobertura',
    preco=45.90,
    estoque=10,
    categoria_id=1
)

p2 = Produto(
    nome='Brigadeiro Gourmet',
    descricao='Brigadeiro de chocolate belga',
    preco=3.50,
    estoque=50,
    categoria_id=2
)

p3 = Produto(
    nome='Torta de Limão',
    descricao='Torta cremosa de limão siciliano',
    preco=38.00,
    estoque=8,
    categoria_id=3
)

db.session.add_all([p1, p2, p3])
db.session.commit()

print("Dados inseridos com sucesso!")
exit()
```

## 🔧 Comandos Úteis do Docker

### Gerenciamento de Containers
```powershell
# Parar todos os serviços
docker-compose down

# Parar e remover volumes (CUIDADO: apaga dados)
docker-compose down -v

# Reiniciar um serviço específico
docker-compose restart catalogo-service

# Reconstruir imagens após mudanças no código
docker-compose build

# Reconstruir e reiniciar
docker-compose up -d --build
```

### Monitoramento
```powershell
# Ver uso de recursos
docker stats

# Inspecionar container
docker inspect catalogo-service

# Executar comando em container
docker exec -it catalogo-service bash
```

### Logs e Debug
```powershell
# Logs em tempo real
docker-compose logs -f --tail=100

# Logs de erro apenas
docker-compose logs | Select-String "ERROR"
```

## 🧪 Testar Tolerância a Falhas

### Teste 1: Queda do Catálogo Primário
```powershell
# Parar serviço primário
docker-compose stop catalogo-service

# Testar réplica (deve continuar funcionando)
curl http://localhost:5011/api/produtos

# Reiniciar primário
docker-compose start catalogo-service
```

### Teste 2: Simulação de Carga
```powershell
# Instalar Apache Bench (se não tiver)
# Usar WSL ou Docker

# Teste de carga - 1000 requisições, 100 concorrentes
docker run --rm --network=confeitaria-network `
    jordi/ab -n 1000 -c 100 http://catalogo-service:5001/api/produtos
```

### Teste 3: Verificar Redis (Persistência de Sessão)
```powershell
# Criar carrinho
$session = Invoke-RestMethod -Uri "http://localhost:5002/api/carrinho/sessao" -Method POST
$sessionId = $session.data.session_id

# Reiniciar serviço de carrinho
docker-compose restart carrinho-service

# Carrinho deve persistir (dados no Redis)
Invoke-RestMethod -Uri "http://localhost:5002/api/carrinho/$sessionId" -Method GET
```

## 🔍 Acessar Ferramentas de Administração

### pgAdmin (PostgreSQL)
1. Acesse: http://localhost:5050
2. Login:
   - Email: `admin@confeitaria.com`
   - Senha: `admin123`
3. Adicionar servidor:
   - Host: `catalogo-db`
   - Port: `5432`
   - User: `catalogo_user`
   - Password: `catalogo_pass`

### Redis Commander
1. Acesse: http://localhost:8081
2. Visualize chaves do carrinho: `carrinho:*`

## 🐛 Troubleshooting

### Problema: Porta já em uso
```powershell
# Verificar processos usando porta 5001
netstat -ano | findstr :5001

# Matar processo (substitua PID)
taskkill /PID <PID> /F
```

### Problema: Container não inicia
```powershell
# Ver logs detalhados
docker-compose logs catalogo-service

# Verificar saúde
docker inspect catalogo-service | Select-String "Health"
```

### Problema: Banco de dados não conecta
```powershell
# Verificar se PostgreSQL está rodando
docker exec -it catalogo-db pg_isready -U catalogo_user

# Acessar banco manualmente
docker exec -it catalogo-db psql -U catalogo_user -d catalogo_db
```

## 📦 Ferramentas Opcionais (Profiles)

Para iniciar com ferramentas de administração:
```powershell
docker-compose --profile tools up -d
```

## 🎯 Próximos Passos

1. ✅ Iniciar todos os serviços
2. ✅ Popular banco de dados
3. ✅ Testar APIs individualmente
4. ✅ Testar comunicação entre serviços
5. ✅ Realizar testes de tolerância a falhas
6. ✅ Documentar resultados para o relatório

## 📝 Estrutura de Testes para o Relatório

### 1. Teste de Funcionalidade
- Criar produto via API
- Adicionar ao carrinho
- Verificar estoque

### 2. Teste de Concorrência
- 100 usuários simultâneos
- Medição de tempo de resposta
- Taxa de erro

### 3. Teste de Tolerância a Falhas
- Derrubar serviço primário
- Verificar failover para réplica
- Tempo de recuperação

### 4. Teste de Escalabilidade
- Aumentar número de réplicas
- Medir throughput
- Comparar desempenho

---

**Última atualização**: Outubro 2025  
**Autor**: Paulo H.
