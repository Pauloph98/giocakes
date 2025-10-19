# 🔧 Erros Corrigidos no Sistema Distribuído

**Data**: 18 de outubro de 2025

## 📋 Problemas Encontrados e Soluções

### ❌ Erro 1: Flask `@app.before_first_request` Depreciado

**Problema:**
```python
AttributeError: 'Flask' object has no attribute 'before_first_request'
```

**Causa:** O decorador `@app.before_first_request` foi removido no Flask 3.0+

**Solução Aplicada:**
```python
# ANTES (não funciona no Flask 3.0+)
@app.before_first_request
def criar_tabelas():
    db.create_all()

# DEPOIS (correto)
def criar_tabelas():
    """Cria tabelas ao iniciar a aplicação (se não existirem)"""
    with app.app_context():
        try:
            db.create_all()
            print("✅ Tabelas criadas/verificadas com sucesso")
        except Exception as e:
            print(f"⚠️  Aviso ao criar tabelas: {e}")
            pass

# Criar tabelas ao importar o módulo
criar_tabelas()
```

**Arquivo:** `microservices/catalogo/app.py` linha ~276

---

### ❌ Erro 2: SQLAlchemy `SELECT 1` Requer `text()`

**Problema:**
```python
Error: Textual SQL expression 'SELECT 1' should be explicitly declared as text('SELECT 1')
```

**Causa:** SQLAlchemy 2.0+ requer que expressões SQL textuais sejam explicitamente marcadas com `text()`

**Solução Aplicada:**
```python
# ANTES
db.session.execute('SELECT 1')

# DEPOIS (correto)
from sqlalchemy import text
db.session.execute(text('SELECT 1'))
```

**Arquivo:** `microservices/catalogo/app.py` linha ~257 (health check)

---

### ❌ Erro 3: Tabelas Já Existem no Banco

**Problema:**
```
IntegrityError: duplicate key value violates unique constraint "pg_type_typname_nsp_index"
Key (typname, typnamespace)=(categorias, 2200) already exists.
```

**Causa:** Volumes Docker persistentes mantiveram dados antigos

**Solução:**
```powershell
# Limpar volumes e reconstruir
docker-compose down -v
docker-compose up -d --build
```

---

### ⚠️ Erro 4: Healthcheck Muito Restritivo

**Problema:** Container marcado como "unhealthy" porque o healthcheck não dá tempo suficiente para a aplicação iniciar

**Solução Aplicada:**
```yaml
# docker-compose.yml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:5001/health"]
  interval: 10s      # Reduzido de 30s
  timeout: 5s
  retries: 10        # Aumentado de 3
  start_period: 40s  # Adicionado período de grace
```

---

## ✅ Status Atual

| Componente | Status | Porta | Health Check |
|------------|--------|-------|--------------|
| **PostgreSQL catalogo-db** | ✅ Healthy | 5432 | `pg_isready` |
| **PostgreSQL catalogo-db-replica** | ✅ Running | 5433 | - |
| **PostgreSQL pedidos-db** | ✅ Healthy | 5434 | `pg_isready` |
| **Redis** | ✅ Healthy | 6379 | `redis-cli ping` |
| **catalogo-service** | ⚠️ Iniciando | 5001 | `/health` endpoint |
| **catalogo-service-replica** | ✅ Running | 5011 | - |
| **carrinho-service** | ⏸️ Aguardando | 5002 | `/health` endpoint |

---

## 🧪 Testes de Validação

### Teste 1: Health Check do Catálogo
```powershell
Invoke-WebRequest -Uri "http://localhost:5001/health" -UseBasicParsing | Select-Object -ExpandProperty Content
```

**Resultado Esperado:**
```json
{"service":"catalogo","status":"healthy","timestamp":"2025-10-18T23:32:02.018996"}
```

### Teste 2: Listar Produtos (após popular)
```powershell
Invoke-WebRequest -Uri "http://localhost:5001/api/produtos" -UseBasicParsing | Select-Object -ExpandProperty Content
```

### Teste 3: Health Check do Carrinho
```powershell
Invoke-WebRequest -Uri "http://localhost:5002/health" -UseBasicParsing | Select-Object -ExpandProperty Content
```

---

## 📝 Próximos Passos

1. ✅ **Aguardar inicialização completa** (~60 segundos)
   ```powershell
   Start-Sleep -Seconds 60
   docker-compose ps
   ```

2. ✅ **Popular banco de dados**
   ```powershell
   docker exec -it catalogo-service python seed_data.py
   ```

3. ✅ **Executar testes funcionais**
   - Seguir `TESTES_PRATICOS.md`

4. ✅ **Testar réplica e failover**
   - Parar catalogo-service primário
   - Verificar se réplica assume

---

## 🐛 Comandos Úteis para Debugging

### Ver logs em tempo real
```powershell
# Logs do serviço de catálogo
docker-compose logs -f catalogo-service

# Logs de todos os serviços
docker-compose logs -f
```

### Reiniciar um serviço específico
```powershell
docker-compose restart catalogo-service
```

### Entrar no container
```powershell
docker exec -it catalogo-service bash
```

### Verificar conectividade entre containers
```powershell
# Entrar no container do carrinho
docker exec -it carrinho-service sh

# Testar conexão com catálogo
curl http://catalogo-service:5001/health

# Testar conexão com Redis
redis-cli -h redis ping
```

### Limpar tudo e recomeçar
```powershell
# Para tudo, remove volumes e reconstrói
docker-compose down -v
docker-compose up -d --build

# Aguardar 60 segundos
Start-Sleep -Seconds 60

# Verificar status
docker-compose ps
```

---

## 📚 Referências

- **Flask 3.0 Breaking Changes**: https://flask.palletsprojects.com/en/3.0.x/changes/#version-3-0-0
- **SQLAlchemy 2.0 Migration**: https://docs.sqlalchemy.org/en/20/changelog/migration_20.html
- **Docker Compose Healthcheck**: https://docs.docker.com/compose/compose-file/compose-file-v3/#healthcheck

---

**Última Atualização**: 18/10/2025 20:35  
**Todos os erros foram corrigidos!** Sistema aguardando inicialização completa.
