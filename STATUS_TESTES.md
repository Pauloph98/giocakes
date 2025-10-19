# ✅ STATUS DO SISTEMA - Como Testar

## 📊 Situação Atual (17/10/2025)

### ✅ O Que Está Funcionando AGORA

| Componente | Status | Como Testar |
|------------|--------|-------------|
| **Django Original** | ✅ Funcionando | `python manage.py runserver` |
| **Banco de Dados** | ✅ Populado | 22 produtos cadastrados |
| **Documentação** | ✅ Completa | 17 arquivos criados |
| **Código Microserviços** | ✅ Pronto | Precisa Docker |
| **Docker** | ❌ Não instalado | Instalar |

---

## 🚀 TESTE RÁPIDO (5 MINUTOS) - O QUE VOCÊ PODE FAZER AGORA

### Teste 1: Verificar Sistema Django Original
```powershell
# Já na pasta do projeto com venv ativado
python manage.py runserver
```

**Abrir navegador**: http://localhost:8000

**O que você verá:**
- ✅ Lista de doces
- ✅ Categorias funcionando
- ✅ Carrinho de compras
- ✅ Sistema completo monolítico

**Isso prova:**
- ✅ Python configurado corretamente
- ✅ Django funcionando
- ✅ Banco de dados OK
- ✅ Sistema base funcional

---

### Teste 2: Verificar Dados no Banco
```powershell
python -c "import os, django; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings'); django.setup(); from confeitaria.models import Doce, Categoria; print(f'Produtos: {Doce.objects.count()}'); print(f'Categorias: {Categoria.objects.count()}')"
```

**Resultado esperado:**
```
Produtos: 22
Categorias: 5
```

---

### Teste 3: Acessar Admin Django
```powershell
# Se ainda não tem superusuário:
python manage.py createsuperuser

# Depois:
python manage.py runserver
```

**Abrir**: http://localhost:8000/admin

**Login com credenciais criadas**

---

## 📋 PRÓXIMOS PASSOS PARA TESTAR MICROSERVIÇOS

### Passo 1: Instalar Docker Desktop (20 minutos)

1. **Download**: https://www.docker.com/products/docker-desktop/
2. **Instalar**: Executar instalador (Next, Next, Finish)
3. **Reiniciar** computador
4. **Verificar instalação**:
```powershell
docker --version
docker-compose --version
```

**Resultado esperado:**
```
Docker version 24.x.x
Docker Compose version 2.x.x
```

---

### Passo 2: Subir Sistema Distribuído (5 minutos)

```powershell
# Na raiz do projeto
cd "C:\Users\PauloH\Documents\trabalho confeitaria\confeitaria-main"

# Subir todos os serviços
docker-compose up -d

# Aguardar inicialização
Start-Sleep -Seconds 30

# Verificar status
docker-compose ps
```

**Resultado esperado:**
```
NAME                   STATUS
catalogo-service       Up
catalogo-service-replica  Up
carrinho-service       Up
catalogo-db            Up
catalogo-db-replica    Up
redis                  Up
pedidos-db             Up
```

---

### Passo 3: Popular Banco dos Microserviços (2 minutos)

```powershell
# Executar script de seed dentro do container
docker exec -it catalogo-service python seed_data.py
```

**Resultado esperado:**
```
Criando tabelas...
✓ 5 categorias criadas
✓ 13 produtos criados
```

---

### Passo 4: Testar APIs REST (5 minutos)

```powershell
# Health Check - Catálogo
Invoke-RestMethod -Uri "http://localhost:5001/health" -Method GET

# Health Check - Carrinho
Invoke-RestMethod -Uri "http://localhost:5002/health" -Method GET

# Listar produtos
Invoke-RestMethod -Uri "http://localhost:5001/api/produtos" -Method GET | ConvertTo-Json -Depth 5

# Criar sessão de carrinho
$response = Invoke-RestMethod -Uri "http://localhost:5002/api/carrinho/sessao" -Method POST
$sessionId = $response.data.session_id
Write-Host "Session ID: $sessionId"

# Adicionar produto ao carrinho
$body = @{
    produto_id = 1
    quantidade = 2
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5002/api/carrinho/$sessionId/adicionar" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body

# Ver carrinho
Invoke-RestMethod -Uri "http://localhost:5002/api/carrinho/$sessionId" -Method GET | ConvertTo-Json -Depth 5
```

---

### Passo 5: Testar Tolerância a Falhas (5 minutos)

```powershell
# 1. Testar primário
Invoke-RestMethod -Uri "http://localhost:5001/api/produtos" -Method GET

# 2. Testar réplica
Invoke-RestMethod -Uri "http://localhost:5011/api/produtos" -Method GET

# 3. Derrubar primário
docker-compose stop catalogo-service

# 4. Verificar que réplica continua funcionando
Invoke-RestMethod -Uri "http://localhost:5011/api/produtos" -Method GET
# ✅ Deve funcionar!

# 5. Reiniciar primário
docker-compose start catalogo-service
```

---

## 📚 Documentação de Testes Detalhada

Após instalar Docker, consulte:

1. **`TESTES_PRATICOS.md`** - Guia completo de testes
2. **`GUIA_EXECUCAO.md`** - Manual de execução
3. **`COMANDOS_UTEIS.md`** - Referência rápida

---

## 🎯 Checklist de Testes para o TCC

### Testes Funcionais
- [ ] Health checks de todos os serviços
- [ ] Listar produtos via API
- [ ] Filtrar produtos (categoria, preço)
- [ ] Criar sessão de carrinho
- [ ] Adicionar itens ao carrinho
- [ ] Atualizar quantidade
- [ ] Remover itens
- [ ] Validação de estoque

### Testes de Integração
- [ ] Carrinho consome API do Catálogo
- [ ] Validação de estoque entre serviços
- [ ] Dados enriquecidos no carrinho

### Testes de Tolerância a Falhas
- [ ] Derrubar serviço primário
- [ ] Réplica continua funcionando
- [ ] Failover automático
- [ ] Recuperação do primário
- [ ] Sem perda de dados

### Testes de Persistência
- [ ] Reiniciar serviço de carrinho
- [ ] Dados persistem no Redis
- [ ] TTL de 24h funcionando

### Testes de Concorrência
- [ ] Múltiplas sessões simultâneas
- [ ] Isolamento entre sessões
- [ ] 10+ usuários concorrentes

### Testes de Performance (Opcional)
- [ ] Apache Bench - 100 requisições
- [ ] Apache Bench - 1000 requisições
- [ ] Latência < 100ms
- [ ] Taxa de sucesso > 99%

---

## 📊 Métricas para o Relatório

### Você Vai Precisar Coletar:

1. **Tempo de resposta médio** (ms)
2. **Throughput** (requisições/segundo)
3. **Taxa de sucesso** (%)
4. **Tempo de failover** (segundos)
5. **Tempo de recuperação** (segundos)
6. **Perda de requisições** durante falha

**Como coletar:**
- Apache Bench para performance
- Medir manualmente failover com `Measure-Command`
- Scripts automatizados em `TESTES_PRATICOS.md`

---

## 🎓 Para a Apresentação do TCC

### Demo ao Vivo (5 minutos)

**Script de Apresentação:**

```powershell
# 1. Mostrar sistema rodando
docker-compose ps

# 2. Demonstrar API funcionando
Invoke-RestMethod -Uri "http://localhost:5001/api/produtos" -Method GET

# 3. Criar carrinho e adicionar produto
$response = Invoke-RestMethod -Uri "http://localhost:5002/api/carrinho/sessao" -Method POST
$sessionId = $response.data.session_id
# ... adicionar produto ...

# 4. DEMO DE TOLERÂNCIA A FALHAS
Write-Host "Derrubando serviço primário..." -ForegroundColor Red
docker-compose stop catalogo-service

Write-Host "Testando réplica..." -ForegroundColor Yellow
Invoke-RestMethod -Uri "http://localhost:5011/api/produtos" -Method GET
Write-Host "✓ Sistema continua funcionando!" -ForegroundColor Green

# 5. Recuperar
docker-compose start catalogo-service
Write-Host "✓ Sistema recuperado!" -ForegroundColor Green
```

---

## ⏰ Cronograma de Testes

### Esta Semana (Até 20/10)
- [x] Criar documentação
- [x] Verificar Django funciona
- [ ] Instalar Docker
- [ ] Testar microserviços básicos

### Semana 2 (21-27/10)
- [ ] Todos os testes funcionais
- [ ] Todos os testes de integração
- [ ] Documentar resultados

### Semana 7 (25/11-01/12)
- [ ] Testes de carga
- [ ] Testes de falha
- [ ] Coletar métricas
- [ ] Gráficos para relatório

---

## 💡 Dica Final

**HOJE (próximos 30 minutos):**
1. ✅ Teste o Django original (já funciona!)
2. ✅ Leia `RESUMO_EXECUTIVO.md`
3. ✅ Baixe Docker Desktop (deixe instalando)

**FINAL DE SEMANA:**
1. ✅ Instale Docker completamente
2. ✅ Execute todos os testes de `TESTES_PRATICOS.md`
3. ✅ Faça screenshot dos resultados

**SEGUNDA-FEIRA:**
1. ✅ Sistema 100% testado e funcionando
2. ✅ Pronto para começar implementação

---

## 📞 Suporte

Se tiver problemas:

1. **Erro no Django**: Verifique `requirements.txt` instalado
2. **Erro no Docker**: Verifique se Docker Desktop está rodando
3. **Porta ocupada**: Use `netstat -ano | findstr :5001` para ver processos
4. **Container não inicia**: Veja logs com `docker-compose logs [serviço]`

**Toda a documentação está criada!** 📚

---

**Última atualização**: 17 Out 2025  
**Status**: ✅ Sistema Django funcionando | ⏳ Aguardando Docker
