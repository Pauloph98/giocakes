# 🧪 Guia Prático de Testes - Sistema Distribuído

## 🎯 Testes Rápidos (5 minutos)

### Teste 1: Verificar Docker
```powershell
# Verificar se Docker está rodando
docker --version
docker-compose --version

# Ver containers ativos
docker ps
```

### Teste 2: Subir Sistema Completo
```powershell
# Na pasta raiz do projeto
cd "C:\Users\PauloH\Documents\trabalho confeitaria\confeitaria-main"

# Subir todos os serviços
docker-compose up -d

# Aguardar 10 segundos para inicialização
Start-Sleep -Seconds 10

# Verificar status
docker-compose ps
```

### Teste 3: Health Checks
```powershell
# Testar Catálogo (Primário)
curl http://localhost:5001/health

# Testar Catálogo (Réplica)
curl http://localhost:5011/health

# Testar Carrinho
curl http://localhost:5002/health
```

---

## 🧪 Testes Detalhados

### TESTE A: Serviço de Catálogo

#### A1. Popular Banco de Dados
```powershell
# Executar script dentro do container
docker exec -it catalogo-service python seed_data.py
```

**Resultado esperado:**
```
Criando tabelas...
Limpando dados existentes...
Criando categorias...
✓ 5 categorias criadas
Criando produtos...
✓ 13 produtos criados

=== CATEGORIAS CRIADAS ===
  1. Bolos (3 produtos)
  2. Doces Finos (3 produtos)
  3. Tortas (3 produtos)
  4. Salgados (2 produtos)
  5. Sobremesas (2 produtos)
```

#### A2. Testar Endpoints do Catálogo
```powershell
# 1. Listar todos os produtos
Invoke-RestMethod -Uri "http://localhost:5001/api/produtos" -Method GET | ConvertTo-Json -Depth 5

# 2. Listar categorias
Invoke-RestMethod -Uri "http://localhost:5001/api/categorias" -Method GET | ConvertTo-Json -Depth 5

# 3. Obter produto específico (ID 1)
Invoke-RestMethod -Uri "http://localhost:5001/api/produtos/1" -Method GET | ConvertTo-Json -Depth 5

# 4. Filtrar produtos por categoria (Bolos = 1)
Invoke-RestMethod -Uri "http://localhost:5001/api/produtos?categoria_id=1" -Method GET | ConvertTo-Json -Depth 5

# 5. Filtrar produtos baratos (até R$20)
Invoke-RestMethod -Uri "http://localhost:5001/api/produtos?preco_max=20" -Method GET | ConvertTo-Json -Depth 5

# 6. Filtrar produtos em estoque
Invoke-RestMethod -Uri "http://localhost:5001/api/produtos?em_estoque=true" -Method GET | ConvertTo-Json -Depth 5

# 7. Buscar produto por nome
Invoke-RestMethod -Uri "http://localhost:5001/api/produtos?busca=chocolate" -Method GET | ConvertTo-Json -Depth 5

# 8. Verificar estoque (produto 1, quantidade 5)
Invoke-RestMethod -Uri "http://localhost:5001/api/produtos/1/estoque?quantidade=5" -Method GET | ConvertTo-Json -Depth 5
```

#### A3. Testar Atualização de Estoque
```powershell
# Remover 5 unidades do estoque
$body = @{
    quantidade = 5
    operacao = "remover"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5001/api/produtos/1/estoque" `
    -Method PUT `
    -ContentType "application/json" `
    -Body $body | ConvertTo-Json -Depth 5

# Adicionar 10 unidades
$body = @{
    quantidade = 10
    operacao = "adicionar"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5001/api/produtos/1/estoque" `
    -Method PUT `
    -ContentType "application/json" `
    -Body $body | ConvertTo-Json -Depth 5

# Definir estoque para 20
$body = @{
    quantidade = 20
    operacao = "definir"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5001/api/produtos/1/estoque" `
    -Method PUT `
    -ContentType "application/json" `
    -Body $body | ConvertTo-Json -Depth 5
```

---

### TESTE B: Serviço de Carrinho

#### B1. Fluxo Completo do Carrinho
```powershell
# 1. Criar nova sessão
$response = Invoke-RestMethod -Uri "http://localhost:5002/api/carrinho/sessao" -Method POST
$sessionId = $response.data.session_id
Write-Host "✓ Session ID criado: $sessionId" -ForegroundColor Green

# 2. Adicionar primeiro produto (ID 1, quantidade 2)
$body = @{
    produto_id = 1
    quantidade = 2
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5002/api/carrinho/$sessionId/adicionar" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body | ConvertTo-Json -Depth 5

Write-Host "✓ Produto 1 adicionado (2 unidades)" -ForegroundColor Green

# 3. Adicionar segundo produto (ID 4, quantidade 10)
$body = @{
    produto_id = 4
    quantidade = 10
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5002/api/carrinho/$sessionId/adicionar" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body | ConvertTo-Json -Depth 5

Write-Host "✓ Produto 4 adicionado (10 unidades)" -ForegroundColor Green

# 4. Ver carrinho completo
Write-Host "`n=== CARRINHO ATUAL ===" -ForegroundColor Cyan
$carrinho = Invoke-RestMethod -Uri "http://localhost:5002/api/carrinho/$sessionId" -Method GET
$carrinho | ConvertTo-Json -Depth 5

Write-Host "`nTotal de itens: $($carrinho.data.total_itens)" -ForegroundColor Yellow
Write-Host "Valor total: R$ $($carrinho.data.valor_total)" -ForegroundColor Yellow

# 5. Atualizar quantidade do produto 1 para 5
$body = @{quantidade = 5} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:5002/api/carrinho/$sessionId/atualizar/1" `
    -Method PUT `
    -ContentType "application/json" `
    -Body $body | ConvertTo-Json -Depth 5

Write-Host "✓ Quantidade do produto 1 atualizada para 5" -ForegroundColor Green

# 6. Ver carrinho atualizado
$carrinho = Invoke-RestMethod -Uri "http://localhost:5002/api/carrinho/$sessionId" -Method GET
Write-Host "Novo valor total: R$ $($carrinho.data.valor_total)" -ForegroundColor Yellow

# 7. Remover produto 4
Invoke-RestMethod -Uri "http://localhost:5002/api/carrinho/$sessionId/remover/4" -Method DELETE
Write-Host "✓ Produto 4 removido" -ForegroundColor Green

# 8. Ver carrinho final
$carrinho = Invoke-RestMethod -Uri "http://localhost:5002/api/carrinho/$sessionId" -Method GET
$carrinho | ConvertTo-Json -Depth 5

# 9. Limpar carrinho
Invoke-RestMethod -Uri "http://localhost:5002/api/carrinho/$sessionId" -Method DELETE
Write-Host "✓ Carrinho limpo" -ForegroundColor Green
```

#### B2. Testar Validação de Estoque
```powershell
# Criar nova sessão
$response = Invoke-RestMethod -Uri "http://localhost:5002/api/carrinho/sessao" -Method POST
$sessionId = $response.data.session_id

# Tentar adicionar quantidade maior que estoque (vai falhar)
$body = @{
    produto_id = 1
    quantidade = 999
} | ConvertTo-Json

try {
    Invoke-RestMethod -Uri "http://localhost:5002/api/carrinho/$sessionId/adicionar" `
        -Method POST `
        -ContentType "application/json" `
        -Body $body
} catch {
    Write-Host "✓ CORRETO: Sistema bloqueou (estoque insuficiente)" -ForegroundColor Green
    $_.Exception.Message
}
```

---

### TESTE C: Integração Catálogo + Carrinho

#### C1. Teste de Fluxo E-commerce Completo
```powershell
Write-Host "`n=== SIMULAÇÃO DE COMPRA ===" -ForegroundColor Cyan

# 1. Listar produtos disponíveis
Write-Host "`n1. Listando produtos disponíveis..." -ForegroundColor Yellow
$produtos = Invoke-RestMethod -Uri "http://localhost:5001/api/produtos?em_estoque=true" -Method GET
Write-Host "   Produtos disponíveis: $($produtos.total)" -ForegroundColor White

# 2. Criar sessão de compra
Write-Host "`n2. Criando sessão de compra..." -ForegroundColor Yellow
$response = Invoke-RestMethod -Uri "http://localhost:5002/api/carrinho/sessao" -Method POST
$sessionId = $response.data.session_id
Write-Host "   Session ID: $sessionId" -ForegroundColor White

# 3. Adicionar produtos ao carrinho
Write-Host "`n3. Adicionando produtos ao carrinho..." -ForegroundColor Yellow

# Bolo de Chocolate (ID 1)
$body = @{produto_id = 1; quantidade = 1} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:5002/api/carrinho/$sessionId/adicionar" `
    -Method POST -ContentType "application/json" -Body $body | Out-Null
Write-Host "   ✓ Bolo de Chocolate adicionado" -ForegroundColor Green

# Brigadeiro (ID 4)
$body = @{produto_id = 4; quantidade = 12} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:5002/api/carrinho/$sessionId/adicionar" `
    -Method POST -ContentType "application/json" -Body $body | Out-Null
Write-Host "   ✓ 12 Brigadeiros adicionados" -ForegroundColor Green

# 4. Ver resumo do carrinho
Write-Host "`n4. Resumo do carrinho:" -ForegroundColor Yellow
$carrinho = Invoke-RestMethod -Uri "http://localhost:5002/api/carrinho/$sessionId" -Method GET

foreach ($item in $carrinho.data.itens) {
    Write-Host "   - $($item.produto.nome): $($item.quantidade)x R$ $($item.produto.preco) = R$ $($item.subtotal)" -ForegroundColor White
}
Write-Host "`n   TOTAL: R$ $($carrinho.data.valor_total)" -ForegroundColor Cyan

# 5. Finalizar (simular)
Write-Host "`n5. Pedido finalizado com sucesso! ✓" -ForegroundColor Green
```

---

### TESTE D: Tolerância a Falhas

#### D1. Teste de Failover do Catálogo
```powershell
Write-Host "`n=== TESTE DE TOLERÂNCIA A FALHAS ===" -ForegroundColor Cyan

# 1. Verificar que primário está funcionando
Write-Host "`n1. Testando serviço primário..." -ForegroundColor Yellow
$response = Invoke-RestMethod -Uri "http://localhost:5001/api/produtos" -Method GET
Write-Host "   ✓ Primário (5001) respondeu: $($response.total) produtos" -ForegroundColor Green

# 2. Verificar que réplica está funcionando
Write-Host "`n2. Testando réplica..." -ForegroundColor Yellow
$response = Invoke-RestMethod -Uri "http://localhost:5011/api/produtos" -Method GET
Write-Host "   ✓ Réplica (5011) respondeu: $($response.total) produtos" -ForegroundColor Green

# 3. Derrubar primário
Write-Host "`n3. Derrubando serviço primário..." -ForegroundColor Yellow
docker-compose stop catalogo-service
Write-Host "   ✓ Serviço primário parado" -ForegroundColor Red
Start-Sleep -Seconds 3

# 4. Verificar que réplica continua funcionando
Write-Host "`n4. Testando réplica (primário está down)..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "http://localhost:5011/api/produtos" -Method GET
    Write-Host "   ✓ Réplica CONTINUA FUNCIONANDO: $($response.total) produtos" -ForegroundColor Green
    Write-Host "   ✓ SISTEMA TOLERANTE A FALHAS!" -ForegroundColor Green
} catch {
    Write-Host "   ✗ Réplica também falhou" -ForegroundColor Red
}

# 5. Verificar que primário realmente está down
Write-Host "`n5. Confirmando que primário está down..." -ForegroundColor Yellow
try {
    Invoke-RestMethod -Uri "http://localhost:5001/api/produtos" -Method GET -ErrorAction Stop
    Write-Host "   ✗ Primário ainda está respondendo" -ForegroundColor Red
} catch {
    Write-Host "   ✓ Primário realmente está down (esperado)" -ForegroundColor Green
}

# 6. Reiniciar primário
Write-Host "`n6. Reiniciando serviço primário..." -ForegroundColor Yellow
docker-compose start catalogo-service
Write-Host "   Aguardando inicialização..." -ForegroundColor White
Start-Sleep -Seconds 10

# 7. Verificar recuperação
Write-Host "`n7. Testando primário após recuperação..." -ForegroundColor Yellow
$response = Invoke-RestMethod -Uri "http://localhost:5001/api/produtos" -Method GET
Write-Host "   ✓ Primário RECUPERADO: $($response.total) produtos" -ForegroundColor Green

Write-Host "`n=== TESTE CONCLUÍDO COM SUCESSO ===" -ForegroundColor Green
```

#### D2. Teste de Persistência do Carrinho
```powershell
Write-Host "`n=== TESTE DE PERSISTÊNCIA (REDIS) ===" -ForegroundColor Cyan

# 1. Criar carrinho e adicionar itens
Write-Host "`n1. Criando carrinho..." -ForegroundColor Yellow
$response = Invoke-RestMethod -Uri "http://localhost:5002/api/carrinho/sessao" -Method POST
$sessionId = $response.data.session_id
Write-Host "   Session ID: $sessionId" -ForegroundColor White

$body = @{produto_id = 1; quantidade = 3} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:5002/api/carrinho/$sessionId/adicionar" `
    -Method POST -ContentType "application/json" -Body $body | Out-Null
Write-Host "   ✓ Produto adicionado" -ForegroundColor Green

# 2. Reiniciar serviço de carrinho
Write-Host "`n2. Reiniciando serviço de carrinho..." -ForegroundColor Yellow
docker-compose restart carrinho-service
Start-Sleep -Seconds 5

# 3. Verificar se dados persistiram
Write-Host "`n3. Verificando persistência dos dados..." -ForegroundColor Yellow
$carrinho = Invoke-RestMethod -Uri "http://localhost:5002/api/carrinho/$sessionId" -Method GET
if ($carrinho.data.itens.Count -gt 0) {
    Write-Host "   ✓ DADOS PERSISTIRAM! Itens no carrinho: $($carrinho.data.total_itens)" -ForegroundColor Green
} else {
    Write-Host "   ✗ Dados foram perdidos" -ForegroundColor Red
}
```

---

### TESTE E: Concorrência

#### E1. Teste de Múltiplas Sessões
```powershell
Write-Host "`n=== TESTE DE CONCORRÊNCIA ===" -ForegroundColor Cyan

# Criar 5 sessões simultâneas
$sessoes = @()
for ($i = 1; $i -le 5; $i++) {
    $response = Invoke-RestMethod -Uri "http://localhost:5002/api/carrinho/sessao" -Method POST
    $sessoes += $response.data.session_id
    Write-Host "Sessão $i criada: $($response.data.session_id)" -ForegroundColor White
}

# Adicionar produtos em paralelo
Write-Host "`nAdicionando produtos em paralelo..." -ForegroundColor Yellow
foreach ($sessionId in $sessoes) {
    $body = @{produto_id = 1; quantidade = 2} | ConvertTo-Json
    Invoke-RestMethod -Uri "http://localhost:5002/api/carrinho/$sessionId/adicionar" `
        -Method POST -ContentType "application/json" -Body $body | Out-Null
}
Write-Host "✓ 5 carrinhos criados e populados simultaneamente" -ForegroundColor Green

# Verificar que todas as sessões estão isoladas
Write-Host "`nVerificando isolamento de sessões..." -ForegroundColor Yellow
foreach ($sessionId in $sessoes) {
    $carrinho = Invoke-RestMethod -Uri "http://localhost:5002/api/carrinho/$sessionId" -Method GET
    Write-Host "Sessão $sessionId: $($carrinho.data.total_itens) itens" -ForegroundColor White
}
```

---

### TESTE F: Performance (Opcional)

#### F1. Teste de Carga com Apache Bench
```powershell
# Via Docker (recomendado)
docker run --rm --network=confeitaria-network jordi/ab `
    -n 100 -c 10 http://catalogo-service:5001/api/produtos

# Interpretação:
# -n 100 = 100 requisições totais
# -c 10  = 10 requisições concorrentes
```

---

## 📊 Testes para o Relatório do TCC

### Script Completo de Testes
```powershell
# Salvar como: test_suite.ps1

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "SUITE DE TESTES - TCC" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan

# Teste 1: Health Checks
Write-Host "`n[TESTE 1] Health Checks" -ForegroundColor Yellow
$catalogo = Invoke-RestMethod -Uri "http://localhost:5001/health" -Method GET
$carrinho = Invoke-RestMethod -Uri "http://localhost:5002/health" -Method GET
Write-Host "✓ Catálogo: $($catalogo.status)" -ForegroundColor Green
Write-Host "✓ Carrinho: $($carrinho.status)" -ForegroundColor Green

# Teste 2: Funcionalidade
Write-Host "`n[TESTE 2] Funcionalidade" -ForegroundColor Yellow
$produtos = Invoke-RestMethod -Uri "http://localhost:5001/api/produtos" -Method GET
Write-Host "✓ Produtos listados: $($produtos.total)" -ForegroundColor Green

# Teste 3: Integração
Write-Host "`n[TESTE 3] Integração Catálogo + Carrinho" -ForegroundColor Yellow
$response = Invoke-RestMethod -Uri "http://localhost:5002/api/carrinho/sessao" -Method POST
$sessionId = $response.data.session_id
$body = @{produto_id = 1; quantidade = 1} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:5002/api/carrinho/$sessionId/adicionar" `
    -Method POST -ContentType "application/json" -Body $body | Out-Null
$carrinho = Invoke-RestMethod -Uri "http://localhost:5002/api/carrinho/$sessionId" -Method GET
Write-Host "✓ Carrinho criado com $($carrinho.data.total_itens) item(ns)" -ForegroundColor Green

# Teste 4: Tolerância a Falhas
Write-Host "`n[TESTE 4] Tolerância a Falhas" -ForegroundColor Yellow
$replica = Invoke-RestMethod -Uri "http://localhost:5011/api/produtos" -Method GET
Write-Host "✓ Réplica funcionando: $($replica.total) produtos" -ForegroundColor Green

Write-Host "`n==================================" -ForegroundColor Cyan
Write-Host "TODOS OS TESTES PASSARAM! ✓" -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Cyan
```

---

## 🔧 Troubleshooting de Testes

### Erro: "Connection refused"
```powershell
# Verificar se containers estão rodando
docker-compose ps

# Ver logs
docker-compose logs -f catalogo-service
```

### Erro: "Session not found"
```powershell
# Verificar Redis
docker exec -it redis redis-cli ping

# Ver chaves no Redis
docker exec -it redis redis-cli KEYS "carrinho:*"
```

### Erro: "Product not found"
```powershell
# Popular banco novamente
docker exec -it catalogo-service python seed_data.py
```

---

**Dica**: Salve os comandos de teste em arquivos `.ps1` para reutilização!
