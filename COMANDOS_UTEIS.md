# ⚡ Comandos Úteis - Referência Rápida

## 🐳 Docker e Docker Compose

### Gerenciar Containers
```powershell
# Subir todos os serviços
docker-compose up -d

# Subir com rebuild
docker-compose up -d --build

# Parar todos os serviços
docker-compose down

# Parar e remover volumes (CUIDADO: apaga dados!)
docker-compose down -v

# Ver status dos containers
docker-compose ps

# Ver logs de todos os serviços
docker-compose logs -f

# Ver logs de um serviço específico
docker-compose logs -f catalogo-service
docker-compose logs -f carrinho-service

# Reiniciar um serviço
docker-compose restart catalogo-service

# Escalar um serviço
docker-compose up -d --scale carrinho-service=3
```

### Gerenciar Containers Individuais
```powershell
# Listar containers rodando
docker ps

# Listar todos os containers
docker ps -a

# Parar container
docker stop catalogo-service

# Iniciar container
docker start catalogo-service

# Remover container
docker rm catalogo-service

# Ver logs de container
docker logs -f catalogo-service

# Executar comando em container
docker exec -it catalogo-service bash
docker exec -it catalogo-service python seed_data.py
```

### Gerenciar Imagens
```powershell
# Listar imagens
docker images

# Remover imagem
docker rmi confeitaria-main-catalogo-service

# Remover imagens não utilizadas
docker image prune

# Build manual de imagem
docker build -t catalogo-service:v1 ./microservices/catalogo
```

### Gerenciar Volumes
```powershell
# Listar volumes
docker volume ls

# Inspecionar volume
docker volume inspect confeitaria-main_catalogo_data

# Remover volume
docker volume rm confeitaria-main_catalogo_data

# Remover volumes não utilizados
docker volume prune
```

### Gerenciar Networks
```powershell
# Listar redes
docker network ls

# Inspecionar rede
docker network inspect confeitaria-network

# Criar rede
docker network create confeitaria-network
```

### Limpeza Geral
```powershell
# Remover tudo que não está sendo usado
docker system prune -a

# Ver uso de espaço
docker system df
```

---

## 🗄️ PostgreSQL

### Acessar Banco de Dados
```powershell
# Acessar PostgreSQL do Catálogo
docker exec -it catalogo-db psql -U catalogo_user -d catalogo_db

# Acessar PostgreSQL de Pedidos
docker exec -it pedidos-db psql -U pedidos_user -d pedidos_db
```

### Comandos SQL Úteis
```sql
-- Listar tabelas
\dt

-- Descrever tabela
\d produtos

-- Listar bancos de dados
\l

-- Conectar a outro banco
\c catalogo_db

-- Sair
\q

-- Contar registros
SELECT COUNT(*) FROM produtos;

-- Ver todos os produtos
SELECT * FROM produtos;

-- Ver produtos com estoque
SELECT nome, preco, estoque FROM produtos WHERE estoque > 0;

-- Ver replicação (no master)
SELECT * FROM pg_stat_replication;

-- Ver se é réplica (no slave)
SELECT pg_is_in_recovery();
```

### Backup e Restore
```powershell
# Fazer backup
docker exec -t catalogo-db pg_dump -U catalogo_user catalogo_db > backup.sql

# Restaurar backup
docker exec -i catalogo-db psql -U catalogo_user -d catalogo_db < backup.sql
```

---

## 🔴 Redis

### Acessar Redis CLI
```powershell
# Acessar Redis
docker exec -it redis redis-cli

# Com senha
docker exec -it redis redis-cli -a senha
```

### Comandos Redis Úteis
```redis
# Testar conexão
PING

# Listar todas as chaves
KEYS *

# Listar chaves de carrinho
KEYS carrinho:*

# Ver valor de uma chave
GET carrinho:123e4567-e89b-12d3-a456-426614174000

# Ver TTL (tempo até expirar)
TTL carrinho:123e4567-e89b-12d3-a456-426614174000

# Deletar chave
DEL carrinho:123e4567-e89b-12d3-a456-426614174000

# Limpar TUDO (CUIDADO!)
FLUSHALL

# Ver informações do servidor
INFO

# Monitorar comandos em tempo real
MONITOR

# Sair
EXIT
```

---

## 🧪 Testes com cURL

### Catálogo
```powershell
# Health check
curl http://localhost:5001/health

# Listar produtos
curl http://localhost:5001/api/produtos

# Listar produtos com filtros
curl "http://localhost:5001/api/produtos?categoria_id=1&preco_max=50"

# Obter produto específico
curl http://localhost:5001/api/produtos/1

# Listar categorias
curl http://localhost:5001/api/categorias

# Verificar estoque
curl "http://localhost:5001/api/produtos/1/estoque?quantidade=5"

# Atualizar estoque
curl -X PUT http://localhost:5001/api/produtos/1/estoque `
  -H "Content-Type: application/json" `
  -d '{\"quantidade\": 10, \"operacao\": \"remover\"}'
```

### Carrinho
```powershell
# Health check
curl http://localhost:5002/health

# Criar sessão
curl -X POST http://localhost:5002/api/carrinho/sessao

# Adicionar item (substitua SESSION_ID)
$sessionId = "cole-aqui-o-session-id"
curl -X POST http://localhost:5002/api/carrinho/$sessionId/adicionar `
  -H "Content-Type: application/json" `
  -d '{\"produto_id\": 1, \"quantidade\": 2}'

# Ver carrinho
curl http://localhost:5002/api/carrinho/$sessionId

# Atualizar quantidade
curl -X PUT http://localhost:5002/api/carrinho/$sessionId/atualizar/1 `
  -H "Content-Type: application/json" `
  -d '{\"quantidade\": 5}'

# Remover item
curl -X DELETE http://localhost:5002/api/carrinho/$sessionId/remover/1

# Limpar carrinho
curl -X DELETE http://localhost:5002/api/carrinho/$sessionId
```

---

## 🧪 Testes com PowerShell (Invoke-RestMethod)

### Catálogo
```powershell
# Listar produtos
Invoke-RestMethod -Uri "http://localhost:5001/api/produtos" -Method GET | ConvertTo-Json -Depth 5

# Criar categoria (se tiver endpoint POST)
$body = @{nome = "Nova Categoria"} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:5001/api/categorias" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body
```

### Carrinho - Fluxo Completo
```powershell
# 1. Criar sessão
$response = Invoke-RestMethod -Uri "http://localhost:5002/api/carrinho/sessao" -Method POST
$sessionId = $response.data.session_id
Write-Host "Session ID: $sessionId"

# 2. Adicionar item
$body = @{
    produto_id = 1
    quantidade = 2
} | ConvertTo-Json

$result = Invoke-RestMethod -Uri "http://localhost:5002/api/carrinho/$sessionId/adicionar" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body
$result | ConvertTo-Json -Depth 5

# 3. Ver carrinho
$carrinho = Invoke-RestMethod -Uri "http://localhost:5002/api/carrinho/$sessionId" -Method GET
$carrinho | ConvertTo-Json -Depth 5

# 4. Atualizar quantidade
$bodyUpdate = @{quantidade = 5} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:5002/api/carrinho/$sessionId/atualizar/1" `
    -Method PUT `
    -ContentType "application/json" `
    -Body $bodyUpdate

# 5. Remover item
Invoke-RestMethod -Uri "http://localhost:5002/api/carrinho/$sessionId/remover/1" -Method DELETE

# 6. Limpar carrinho
Invoke-RestMethod -Uri "http://localhost:5002/api/carrinho/$sessionId" -Method DELETE
```

---

## 🧪 Testes de Performance

### Apache Bench (via Docker)
```powershell
# Teste básico - 100 requisições, 10 concorrentes
docker run --rm --network=confeitaria-network jordi/ab `
  -n 100 -c 10 http://catalogo-service:5001/api/produtos

# Teste de carga - 1000 requisições, 100 concorrentes
docker run --rm --network=confeitaria-network jordi/ab `
  -n 1000 -c 100 http://catalogo-service:5001/api/produtos

# Com verbosidade
docker run --rm --network=confeitaria-network jordi/ab `
  -n 1000 -c 100 -v 2 http://catalogo-service:5001/api/produtos
```

### Script de Teste de Falha
```powershell
# Script: test_failover.ps1
for ($i=1; $i -le 5; $i++) {
    Write-Host "`n=== Teste $i ===" -ForegroundColor Yellow
    
    # Fazer requisições
    $response = curl http://localhost:5001/api/produtos
    Write-Host "Primário respondeu: $($response.StatusCode)" -ForegroundColor Green
    
    # Derrubar primário
    docker-compose stop catalogo-service
    Write-Host "Primário derrubado!" -ForegroundColor Red
    Start-Sleep -Seconds 2
    
    # Testar réplica
    $responseReplica = curl http://localhost:5011/api/produtos
    Write-Host "Réplica respondeu: $($responseReplica.StatusCode)" -ForegroundColor Green
    
    # Reiniciar primário
    docker-compose start catalogo-service
    Write-Host "Primário reiniciado!" -ForegroundColor Cyan
    Start-Sleep -Seconds 5
}
```

---

## 🐍 Python - Desenvolvimento Local

### Criar Ambiente Virtual
```powershell
# Criar venv
python -m venv venv

# Ativar venv
.\venv\Scripts\Activate.ps1

# Desativar
deactivate

# Instalar dependências
pip install -r requirements.txt

# Atualizar requirements
pip freeze > requirements.txt
```

### Executar Serviços Localmente
```powershell
# Catálogo (na pasta microservices/catalogo)
python app.py

# Popular banco
python seed_data.py

# Carrinho (na pasta microservices/carrinho)
python app.py
```

---

## 📊 Monitoramento e Debug

### Verificar Saúde dos Serviços
```powershell
# Script: health_check.ps1
$services = @(
    @{Name="Catálogo"; Url="http://localhost:5001/health"},
    @{Name="Catálogo Réplica"; Url="http://localhost:5011/health"},
    @{Name="Carrinho"; Url="http://localhost:5002/health"}
)

foreach ($service in $services) {
    try {
        $response = Invoke-RestMethod -Uri $service.Url -Method GET -ErrorAction Stop
        Write-Host "✓ $($service.Name): HEALTHY" -ForegroundColor Green
    } catch {
        Write-Host "✗ $($service.Name): UNHEALTHY" -ForegroundColor Red
    }
}
```

### Ver Uso de Recursos
```powershell
# CPU, memória, I/O em tempo real
docker stats

# Apenas catálogo
docker stats catalogo-service

# Com formato customizado
docker stats --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"
```

### Inspecionar Container
```powershell
# Ver configuração completa
docker inspect catalogo-service

# Ver apenas IP
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' catalogo-service

# Ver variáveis de ambiente
docker inspect -f '{{.Config.Env}}' catalogo-service
```

---

## 🔧 Troubleshooting

### Porta em Uso
```powershell
# Ver processo usando porta 5001
netstat -ano | findstr :5001

# Matar processo (substitua PID)
taskkill /PID <PID> /F
```

### Container Não Inicia
```powershell
# Ver logs detalhados
docker-compose logs catalogo-service

# Ver eventos do container
docker events --filter container=catalogo-service

# Tentar iniciar manualmente para ver erro
docker run -it --rm confeitaria-main-catalogo-service bash
```

### Banco de Dados Não Conecta
```powershell
# Verificar se PostgreSQL está rodando
docker exec -it catalogo-db pg_isready -U catalogo_user

# Ver logs do PostgreSQL
docker logs catalogo-db

# Tentar conexão manual
docker exec -it catalogo-db psql -U catalogo_user -d catalogo_db
```

### Redis Não Conecta
```powershell
# Testar Redis
docker exec -it redis redis-cli ping

# Ver configuração
docker exec -it redis redis-cli CONFIG GET *

# Ver logs
docker logs redis
```

---

## 📝 Git

### Comandos Básicos
```powershell
# Status
git status

# Adicionar arquivos
git add .

# Commit
git commit -m "Descrição da mudança"

# Push
git push origin main

# Pull
git pull origin main

# Ver histórico
git log --oneline

# Criar branch
git checkout -b feature/nova-funcionalidade

# Mudar de branch
git checkout main

# Merge
git merge feature/nova-funcionalidade
```

### Versionamento de Releases
```powershell
# Criar tag
git tag -a v1.0.0 -m "Release 1.0.0"

# Push da tag
git push origin v1.0.0

# Listar tags
git tag
```

---

## 📦 Exports e Backups

### Exportar Dados
```powershell
# Exportar produtos para JSON
docker exec -it catalogo-db psql -U catalogo_user -d catalogo_db `
  -c "COPY (SELECT row_to_json(t) FROM produtos t) TO STDOUT" > produtos.json

# Backup completo
docker exec -t catalogo-db pg_dump -U catalogo_user catalogo_db > backup_$(Get-Date -Format "yyyyMMdd").sql
```

### Backup Automatizado
```powershell
# Script: backup.ps1
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backupDir = "backups"

if (!(Test-Path $backupDir)) {
    New-Item -ItemType Directory -Path $backupDir
}

# Backup Catálogo
docker exec -t catalogo-db pg_dump -U catalogo_user catalogo_db > "$backupDir/catalogo_$timestamp.sql"

# Backup Pedidos
docker exec -t pedidos-db pg_dump -U pedidos_user pedidos_db > "$backupDir/pedidos_$timestamp.sql"

Write-Host "Backups criados em $backupDir/" -ForegroundColor Green
```

---

## 🎯 Comandos para Apresentação do TCC

### 1. Demonstração Rápida
```powershell
# Subir sistema
docker-compose up -d

# Aguardar 10 segundos
Start-Sleep -Seconds 10

# Health check
curl http://localhost:5001/health
curl http://localhost:5002/health

# Listar produtos
curl http://localhost:5001/api/produtos | ConvertTo-Json
```

### 2. Demonstração de Tolerância a Falhas
```powershell
# Loop de requisições
while ($true) {
    $response = curl http://localhost:5001/api/produtos
    Write-Host "Status: $($response.StatusCode)" -ForegroundColor Green
    Start-Sleep -Seconds 1
}

# Em outro terminal, derrubar primário
docker-compose stop catalogo-service

# Requisições continuam via réplica em http://localhost:5011
```

### 3. Demonstração de Escalabilidade
```powershell
# Escalar carrinho
docker-compose up -d --scale carrinho-service=3

# Ver instâncias
docker ps | Select-String "carrinho"

# Teste de carga
docker run --rm --network=confeitaria-network jordi/ab `
  -n 1000 -c 100 http://carrinho-service:5002/health
```

---

**Última atualização**: 17 Out 2025  
**Autor**: Paulo H.
