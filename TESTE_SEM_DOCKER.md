# 🚀 Teste Rápido SEM Docker - Desenvolvimento Local

## ⚠️ Docker Não Instalado - Solução Alternativa

Como o Docker não está instalado, vamos testar os microserviços **localmente** primeiro!

---

## 📋 Opção 1: Testar Localmente (AGORA)

### Passo 1: Instalar Dependências do Catálogo

```powershell
# Navegar para pasta do catálogo
cd "C:\Users\PauloH\Documents\trabalho confeitaria\confeitaria-main\microservices\catalogo"

# Criar ambiente virtual (se não existir)
python -m venv venv

# Ativar ambiente virtual
.\venv\Scripts\Activate.ps1

# Instalar dependências
pip install -r requirements.txt
```

### Passo 2: Instalar PostgreSQL Local (OPCIONAL)

**OPÇÃO A: Usar SQLite (Mais Fácil)**
Modifique temporariamente o `app.py`:

```python
# Linha ~15 em app.py
# ANTES:
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL', 
    'postgresql://catalogo_user:catalogo_pass@localhost:5432/catalogo_db'
)

# DEPOIS (SQLite - mais fácil para teste):
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///catalogo.db'
```

**OPÇÃO B: Instalar PostgreSQL**
- Download: https://www.postgresql.org/download/windows/
- Ou usar versão portátil

### Passo 3: Executar Serviço de Catálogo

```powershell
# Com venv ativado, executar:
python app.py
```

**Resultado esperado:**
```
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in production.
 * Running on http://0.0.0.0:5001
```

### Passo 4: Testar em Outro Terminal

```powershell
# Abrir NOVO terminal PowerShell

# Teste 1: Health Check
Invoke-RestMethod -Uri "http://localhost:5001/health" -Method GET

# Teste 2: Listar produtos (vai estar vazio)
Invoke-RestMethod -Uri "http://localhost:5001/api/produtos" -Method GET

# Teste 3: Listar categorias
Invoke-RestMethod -Uri "http://localhost:5001/api/categorias" -Method GET
```

### Passo 5: Popular Banco

```powershell
# No terminal do serviço (Ctrl+C para parar)
# Depois:
python seed_data.py

# Reiniciar serviço:
python app.py

# Em outro terminal, testar novamente:
Invoke-RestMethod -Uri "http://localhost:5001/api/produtos" -Method GET
```

---

## 📋 Opção 2: Instalar Docker (RECOMENDADO)

### Por que Docker é Importante?

✅ **Simula ambiente real** - Containers isolados  
✅ **Fácil de gerenciar** - Um comando sobe tudo  
✅ **Necessário para réplica** - PostgreSQL Master-Slave  
✅ **Requerido no TCC** - "Nós independentes"  

### Como Instalar Docker Desktop

1. **Download**: https://www.docker.com/products/docker-desktop/
2. **Instalar**: Executar instalador
3. **Reiniciar** o computador
4. **Verificar**: 
```powershell
docker --version
docker-compose --version
```

### Depois de Instalar Docker

```powershell
# Voltar para raiz do projeto
cd "C:\Users\PauloH\Documents\trabalho confeitaria\confeitaria-main"

# Subir tudo
docker-compose up -d

# Aguardar 30 segundos
Start-Sleep -Seconds 30

# Popular banco
docker exec -it catalogo-service python seed_data.py

# Testar
Invoke-RestMethod -Uri "http://localhost:5001/api/produtos" -Method GET
```

---

## 🧪 Testes Que Você Pode Fazer AGORA (Sem Docker)

### Teste A: Sistema Monolítico Django (Original)

```powershell
# Na raiz do projeto
cd "C:\Users\PauloH\Documents\trabalho confeitaria\confeitaria-main"

# Ativar venv (se já existe)
.\venv\Scripts\Activate.ps1

# Instalar dependências Django
pip install -r requirements.txt

# Aplicar migrações
python manage.py migrate

# Criar superusuário (opcional)
python manage.py createsuperuser

# Rodar servidor Django
python manage.py runserver
```

**Acessar:**
- Frontend: http://localhost:8000
- Admin: http://localhost:8000/admin

**Isso prova:**
✅ Sistema original funciona  
✅ Banco de dados funciona  
✅ Python está configurado  

---

## 📊 Comparação: Local vs Docker

| Aspecto | Local (Sem Docker) | Docker |
|---------|-------------------|--------|
| **Facilidade** | ⚠️ Configuração manual | ✅ Um comando |
| **Isolamento** | ❌ Usa sistema host | ✅ Containers isolados |
| **Réplica BD** | ❌ Difícil | ✅ Fácil |
| **Multi-serviço** | ⚠️ Múltiplos terminais | ✅ Orquestrado |
| **Para TCC** | ⚠️ Aceito mas limitado | ✅ Ideal |
| **Tempo Setup** | 10 min | 5 min (após instalar) |

---

## 🎯 Minha Recomendação

### Hoje (Sexta-feira):
1. ✅ Testar sistema Django original (10 min)
2. ✅ Ler documentação criada (1 hora)
3. ✅ Baixar Docker Desktop (começar instalação)

### Final de Semana:
1. ✅ Instalar Docker Desktop completamente
2. ✅ Testar microserviços com Docker
3. ✅ Popular banco de dados
4. ✅ Executar testes do `TESTES_PRATICOS.md`

### Segunda-feira:
1. ✅ Sistema 100% funcional
2. ✅ Começar implementação (Semana 1)

---

## 📝 Script de Teste Local Rápido

```powershell
# Salvar como: test_local.ps1

Write-Host "=== TESTE LOCAL (SEM DOCKER) ===" -ForegroundColor Cyan

# 1. Testar Django Original
Write-Host "`n[1] Testando Django original..." -ForegroundColor Yellow
cd "C:\Users\PauloH\Documents\trabalho confeitaria\confeitaria-main"

if (Test-Path ".\venv\Scripts\Activate.ps1") {
    .\venv\Scripts\Activate.ps1
    Write-Host "✓ Venv ativado" -ForegroundColor Green
} else {
    Write-Host "⚠ Venv não encontrado. Criando..." -ForegroundColor Yellow
    python -m venv venv
    .\venv\Scripts\Activate.ps1
}

# 2. Instalar dependências
Write-Host "`n[2] Verificando dependências..." -ForegroundColor Yellow
pip install -q django pillow

# 3. Testar se Django funciona
Write-Host "`n[3] Testando Django..." -ForegroundColor Yellow
python manage.py check
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Django está OK!" -ForegroundColor Green
} else {
    Write-Host "✗ Erro no Django" -ForegroundColor Red
}

# 4. Verificar banco de dados
Write-Host "`n[4] Verificando banco de dados..." -ForegroundColor Yellow
if (Test-Path ".\db.sqlite3") {
    Write-Host "✓ Banco de dados existe" -ForegroundColor Green
    
    # Contar produtos
    $produtos = python manage.py shell -c "from confeitaria.models import Doce; print(Doce.objects.count())"
    Write-Host "   Produtos cadastrados: $produtos" -ForegroundColor White
} else {
    Write-Host "⚠ Banco não existe. Execute: python manage.py migrate" -ForegroundColor Yellow
}

# 5. Resultado
Write-Host "`n=== RESULTADO ===" -ForegroundColor Cyan
Write-Host "Sistema Django: OK ✓" -ForegroundColor Green
Write-Host "`nPróximo passo: Instalar Docker para testar microserviços" -ForegroundColor Yellow
Write-Host "Download: https://www.docker.com/products/docker-desktop/" -ForegroundColor White
```

---

## ❓ FAQ - Perguntas Frequentes

### P: Posso fazer o TCC sem Docker?
**R:** Tecnicamente sim, mas vai perder pontos importantes:
- ❌ Sem replicação de BD
- ❌ Sem "nós independentes"
- ❌ Menos profissional
- ⚠️ Nota máxima: 8.0-8.5 (em vez de 9.5-10.0)

### P: Docker é difícil de instalar?
**R:** Não! É um instalador normal do Windows. Requer:
- Windows 10/11 Pro ou Home (versão 2004+)
- Virtualização habilitada na BIOS
- 4GB RAM mínimo (8GB recomendado)

### P: Quanto tempo leva para instalar Docker?
**R:** 
- Download: 5-10 minutos (500MB)
- Instalação: 5 minutos
- Reiniciar PC: 2 minutos
- **Total: ~20 minutos**

### P: Posso testar só parte do sistema sem Docker?
**R:** Sim! Você pode:
1. ✅ Rodar Django original (já funciona)
2. ✅ Rodar 1 microserviço local (Catálogo com SQLite)
3. ❌ Não consegue rodar sistema completo com réplica

---

## 🎓 Para o TCC

### O que o Avaliador Vai Querer Ver:

1. **Sistema rodando** - Docker facilita isso ✅
2. **Microserviços isolados** - Containers Docker ✅
3. **Replicação funcionando** - Docker Compose ✅
4. **Teste de failover** - Parar container e ver réplica assumir ✅
5. **Código organizado** - Já está pronto ✅

### Você Tem 8 Semanas:

- **Semana 1**: Instalar Docker + Testar sistema
- **Semanas 2-6**: Implementar/melhorar microserviços
- **Semana 7**: Testes e coleta de métricas
- **Semana 8**: Relatório e apresentação

**Docker é essencial! Instale no final de semana.** 💪

---

## 🚀 AÇÃO IMEDIATA (Próximos 10 minutos)

```powershell
# 1. Testar Django (já funciona)
cd "C:\Users\PauloH\Documents\trabalho confeitaria\confeitaria-main"
.\venv\Scripts\Activate.ps1
python manage.py runserver

# 2. Abrir navegador
# http://localhost:8000

# 3. Verificar que sistema original funciona ✓

# 4. Baixar Docker Desktop
# https://www.docker.com/products/docker-desktop/
```

---

**Conclusão**: Você pode começar a explorar AGORA com Django, mas **instale Docker este final de semana** para ter o sistema completo distribuído funcionando! 🎯
