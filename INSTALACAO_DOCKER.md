# 🐳 Guia de Instalação do Docker Desktop no Windows

**Data**: 17 de outubro de 2025  
**Sistema**: Windows 11  
**Versão necessária**: Docker Desktop 4.x ou superior

---

## 📋 Pré-requisitos

Antes de instalar o Docker, verifique:

### 1. **Requisitos de Sistema**
- ✅ Windows 10 64-bit: Pro, Enterprise ou Education (Build 19041 ou superior)
- ✅ Windows 11 64-bit
- ✅ Mínimo 4GB de RAM (recomendado 8GB)
- ✅ Virtualização habilitada na BIOS

### 2. **Verificar Virtualização**

Abra o **Gerenciador de Tarefas** (Ctrl + Shift + Esc):
- Vá em **Desempenho** → **CPU**
- Verifique se **"Virtualização: Habilitada"**

Se estiver **Desabilitada**:
- Reinicie o computador
- Entre na BIOS (geralmente F2, F10, F12 ou Del)
- Procure por "Intel VT-x" ou "AMD-V"
- Habilite e salve

---

## 🚀 Passo a Passo da Instalação

### **Passo 1: Download do Docker Desktop**

1. Acesse o site oficial:
   ```
   https://www.docker.com/products/docker-desktop/
   ```

2. Clique em **"Download for Windows"**

3. Aguarde o download do arquivo `Docker Desktop Installer.exe` (~500MB)

### **Passo 2: Executar o Instalador**

1. Localize o arquivo baixado e execute como **Administrador**
   - Clique com botão direito → **"Executar como administrador"**

2. Na tela de configuração:
   - ✅ **Marque**: "Use WSL 2 instead of Hyper-V" (recomendado)
   - ✅ **Marque**: "Add shortcut to desktop"
   
3. Clique em **"Ok"** para iniciar a instalação

4. Aguarde a instalação (~5-10 minutos)

### **Passo 3: Reiniciar o Computador**

⚠️ **IMPORTANTE**: Após a instalação, você **DEVE** reiniciar o computador!

```powershell
# Após reiniciar, o Docker Desktop iniciará automaticamente
```

### **Passo 4: Configuração Inicial**

1. Aceite os **Termos de Serviço** do Docker

2. Na tela de boas-vindas:
   - Pode pular o tutorial (já temos os arquivos prontos!)
   - Não precisa criar conta Docker Hub agora

3. Aguarde o Docker iniciar (ícone da baleia na bandeja do sistema)
   - ⚪ Animado = Iniciando
   - 🟢 Verde = Pronto para usar!

---

## ✅ Verificar a Instalação

Abra o **PowerShell** e execute:

```powershell
# Verificar versão do Docker
docker --version

# Verificar versão do Docker Compose
docker-compose --version

# Testar funcionamento básico
docker run hello-world
```

**Saída esperada**:
```
Docker version 24.0.x, build xxxxx
Docker Compose version v2.x.x
Hello from Docker!
This message shows that your installation appears to be working correctly.
```

---

## 🔧 Configurações Recomendadas

### **1. Recursos do Docker Desktop**

Abra o Docker Desktop → ⚙️ **Settings** → **Resources**:

- **CPU**: Mínimo 2, Recomendado 4
- **Memory**: Mínimo 4GB, Recomendado 8GB
- **Swap**: 1GB
- **Disk image size**: 60GB (padrão)

### **2. Habilitar Kubernetes (Opcional)**

Se quiser explorar orquestração mais avançada:
- Settings → **Kubernetes** → ✅ Enable Kubernetes

⚠️ **NÃO é necessário para o TCC** (usaremos apenas Docker Compose)

---

## 🎯 Próximos Passos Após Instalação

### **1. Testar o Sistema Distribuído (5 minutos)**

```powershell
# 1. Entre no diretório do projeto
cd "C:\Users\PauloH\Documents\trabalho confeitaria\confeitaria-main"

# 2. Ative o ambiente virtual
venv\Scripts\Activate.ps1

# 3. Inicie todos os serviços
docker-compose up -d

# 4. Verifique se todos os containers estão rodando
docker-compose ps
```

**Saída esperada**: 9 containers rodando (catalogo, carrinho, bancos de dados, etc.)

### **2. Popular os Bancos de Dados**

```powershell
# Popular o banco do catálogo com dados de exemplo
docker exec -it catalogo-service python seed_data.py
```

### **3. Executar os Testes**

Siga o guia completo em `TESTES_PRATICOS.md`:

```powershell
# Teste rápido de saúde dos serviços
Invoke-WebRequest -Uri "http://localhost:5001/health" -UseBasicParsing | Select-Object -ExpandProperty Content
Invoke-WebRequest -Uri "http://localhost:5002/health" -UseBasicParsing | Select-Object -ExpandProperty Content
```

---

## 🐛 Solução de Problemas Comuns

### **Problema 1: "Hardware assisted virtualization is not enabled"**

**Solução**:
1. Entre na BIOS do computador
2. Habilite "Intel VT-x" ou "AMD-V"
3. Salve e reinicie

### **Problema 2: "WSL 2 installation is incomplete"**

**Solução**:
```powershell
# Instalar WSL 2 manualmente
wsl --install
wsl --set-default-version 2

# Reiniciar o computador
```

### **Problema 3: "Docker Desktop failed to start"**

**Solução**:
1. Abra o **Gerenciador de Tarefas**
2. Finalize todos os processos "Docker Desktop"
3. Reinicie o Docker Desktop como Administrador

### **Problema 4: "Port is already allocated"**

**Solução**:
```powershell
# Verificar portas em uso
netstat -ano | findstr ":5001"
netstat -ano | findstr ":5002"

# Se alguma porta estiver ocupada:
# 1. Finalize o processo usando a porta, OU
# 2. Edite docker-compose.yml para usar outra porta
```

### **Problema 5: Containers não iniciam**

**Solução**:
```powershell
# Ver logs detalhados
docker-compose logs -f

# Reiniciar containers específicos
docker-compose restart catalogo-service
docker-compose restart carrinho-service

# Recriar tudo do zero
docker-compose down -v
docker-compose up -d --build
```

---

## 📚 Comandos Úteis do Docker

### **Gerenciamento de Containers**

```powershell
# Listar containers em execução
docker ps

# Listar TODOS os containers (incluindo parados)
docker ps -a

# Parar todos os containers
docker-compose down

# Parar e remover volumes (⚠️ apaga dados)
docker-compose down -v

# Reiniciar um serviço específico
docker-compose restart catalogo-service

# Ver logs de um serviço
docker-compose logs -f catalogo-service

# Executar comando dentro de um container
docker exec -it catalogo-service bash
```

### **Gerenciamento de Imagens**

```powershell
# Listar imagens
docker images

# Remover imagens não utilizadas
docker image prune -a

# Rebuild de uma imagem específica
docker-compose build catalogo-service
docker-compose up -d catalogo-service
```

### **Limpeza Geral**

```powershell
# Remover containers parados
docker container prune

# Remover volumes não utilizados
docker volume prune

# Limpeza completa (⚠️ cuidado!)
docker system prune -a --volumes
```

---

## 📊 Monitoramento

### **1. Docker Desktop Dashboard**

- Abra o Docker Desktop
- Veja containers em execução
- Acesse logs em tempo real
- Monitore uso de CPU/RAM

### **2. Ferramentas Web Incluídas**

Após `docker-compose up -d`:

- **pgAdmin** (PostgreSQL): http://localhost:5050
  - Email: `admin@confeitaria.com`
  - Senha: `admin123`

- **Redis Commander**: http://localhost:8081

---

## 🎓 Integração com o TCC

### **Por que o Docker é essencial?**

1. **✅ Requisito: Sistemas Distribuídos**
   - Docker permite executar múltiplos serviços isolados
   - Simula ambiente de produção real

2. **✅ Requisito: Replicação**
   - `docker-compose.yml` configura PostgreSQL Master-Slave
   - Demonstra alta disponibilidade

3. **✅ Requisito: Tolerância a Falhas**
   - Containers podem ser reiniciados automaticamente
   - Testes de failover ficam simples

4. **✅ Requisito: Escalabilidade**
   - Fácil criar réplicas de serviços
   - `docker-compose up --scale catalogo-service=3`

### **Métricas para o Relatório**

Com Docker rodando, você pode coletar:

```powershell
# Tempo de resposta médio
Measure-Command { Invoke-WebRequest -Uri "http://localhost:5001/api/produtos" }

# Uso de recursos
docker stats

# Teste de carga (Apache Bench)
docker run --rm jordi/ab ab -n 1000 -c 10 http://host.docker.internal:5001/api/produtos
```

---

## 📝 Checklist de Instalação

Use este checklist para garantir que tudo está funcionando:

- [ ] Docker Desktop instalado
- [ ] Computador reiniciado
- [ ] `docker --version` retorna versão
- [ ] `docker-compose --version` retorna versão
- [ ] `docker run hello-world` funciona
- [ ] Recursos alocados (8GB RAM)
- [ ] `docker-compose up -d` inicia 9 containers
- [ ] `docker-compose ps` mostra todos "Up"
- [ ] APIs respondem: `/health` retorna `{"status": "healthy"}`
- [ ] Dados populados: `seed_data.py` executado
- [ ] Testes funcionais passam (seguir `TESTES_PRATICOS.md`)

---

## 🆘 Suporte

### **Documentação Oficial**
- Docker Docs: https://docs.docker.com/
- Docker Desktop Windows: https://docs.docker.com/desktop/install/windows-install/

### **Arquivos do Projeto**
- `README.md` - Visão geral do sistema
- `GUIA_EXECUCAO.md` - Como executar após Docker instalado
- `TESTES_PRATICOS.md` - Testes completos
- `COMANDOS_UTEIS.md` - Referência rápida

### **Comunidade**
- Docker Community: https://forums.docker.com/
- Stack Overflow: https://stackoverflow.com/questions/tagged/docker

---

## ⏱️ Tempo Total Estimado

| Etapa | Tempo |
|-------|-------|
| Download | 5-10 min |
| Instalação | 10-15 min |
| Reinicialização | 2-3 min |
| Configuração inicial | 5 min |
| Testes de verificação | 5 min |
| **TOTAL** | **~30-40 min** |

---

## 🎯 Resultado Final

Após completar este guia, você terá:

✅ Docker Desktop funcionando  
✅ 9 containers do sistema distribuído rodando  
✅ 3 microserviços comunicando via REST  
✅ PostgreSQL com replicação Master-Slave  
✅ Redis para gerenciamento de sessões  
✅ Sistema pronto para testes e demonstração no TCC  

---

**Próximo arquivo a ler**: `GUIA_EXECUCAO.md` (como executar o sistema completo)

**Dúvidas?** Consulte `STATUS_TESTES.md` para ver o status atual e próximos passos.

---

**Boa sorte com a instalação! 🚀**
