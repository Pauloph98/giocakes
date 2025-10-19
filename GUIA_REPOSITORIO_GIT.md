# 🔗 Guia Completo: Repositório Git para o TCC

**Projeto**: Sistema Distribuído de Confeitaria  
**Requisito TCC**: Código-fonte em repositório Git (30% da nota)

---

## ❓ O que é um Repositório Git?

### **Repositório Git = Pasta com histórico de mudanças**

É onde você guarda:
- ✅ Todo o código-fonte
- ✅ Documentação
- ✅ Histórico de alterações (quem mudou o quê e quando)
- ✅ Versões anteriores do projeto

### **GitHub = Site para hospedar repositórios Git**

Pense assim:
- **Git** = Sistema de controle de versão (ferramenta)
- **GitHub** = Site onde o repositório fica online (como Google Drive para código)

**Alternativas ao GitHub:**
- GitLab (https://gitlab.com)
- Bitbucket (https://bitbucket.org)
- Azure DevOps

---

## ✅ SIM, é para colocar no GitHub!

**Para o TCC, você deve:**

1. ✅ Criar conta no GitHub
2. ✅ Criar um repositório público
3. ✅ Subir todo o código do projeto
4. ✅ Incluir o link do repositório no relatório
5. ✅ A banca vai acessar e avaliar

---

## 🚀 Passo a Passo: Criando seu Repositório

### **Etapa 1: Criar Conta no GitHub** (5 minutos)

1. Acesse: **https://github.com**
2. Clique em **"Sign up"**
3. Preencha:
   - Email
   - Senha
   - Nome de usuário (exemplo: `paulo-silva-tcc`)
4. Verifique seu email
5. ✅ Pronto!

---

### **Etapa 2: Instalar Git no Windows** (5 minutos)

**Verificar se já tem Git:**
```powershell
git --version
```

**Se não tiver, instalar:**
```powershell
# Opção 1: Winget (recomendado)
winget install Git.Git

# Opção 2: Chocolatey
choco install git

# Opção 3: Download manual
# https://git-scm.com/download/win
```

**Configurar Git:**
```powershell
# Seu nome (aparece nos commits)
git config --global user.name "Paulo Silva"

# Seu email (mesmo do GitHub)
git config --global user.email "seu-email@gmail.com"

# Verificar
git config --list
```

---

### **Etapa 3: Criar Repositório no GitHub** (3 minutos)

1. Login no GitHub
2. Clicar no **"+"** no canto superior direito
3. **"New repository"**
4. Preencher:
   ```
   Repository name: confeitaria-distribuida-tcc
   Description: Sistema Distribuído de E-commerce para Confeitaria - TCC Sistemas Distribuídos
   ✅ Public (público para a banca avaliar)
   ❌ NÃO marcar "Add a README" (já temos)
   ❌ NÃO adicionar .gitignore (já temos)
   ```
5. **"Create repository"**

---

### **Etapa 4: Preparar Projeto para Git** (5 minutos)

```powershell
# Entrar na pasta do projeto
cd "C:\Users\PauloH\Documents\trabalho confeitaria\confeitaria-main"

# Criar arquivo .gitignore (ignorar arquivos desnecessários)
@"
# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
pip-log.txt
pip-delete-this-directory.txt

# Django
*.log
*.pot
*.pyc
local_settings.py
db.sqlite3
db.sqlite3-journal
/media
/static

# Docker
.dockerignore

# IDEs
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Env files
.env
.env.local
"@ | Out-File -FilePath .gitignore -Encoding utf8
```

---

### **Etapa 5: Subir Código para o GitHub** (10 minutos)

```powershell
# 1. Inicializar repositório Git local
git init

# 2. Adicionar todos os arquivos
git add .

# 3. Ver o que será commitado
git status

# 4. Fazer o primeiro commit
git commit -m "feat: Sistema distribuído completo - Catálogo, Carrinho e Replicação

- Microserviço de Catálogo (Flask + PostgreSQL)
- Microserviço de Carrinho (Flask + Redis)
- Replicação PostgreSQL Master-Slave
- Réplica do serviço de Catálogo
- Docker Compose com 9 serviços
- Documentação completa
- Testes de concorrência e failover"

# 5. Adicionar repositório remoto do GitHub
# Substitua SEU-USUARIO pelo seu usuário do GitHub!
git remote add origin https://github.com/SEU-USUARIO/confeitaria-distribuida-tcc.git

# 6. Renomear branch para 'main'
git branch -M main

# 7. Enviar código para o GitHub
git push -u origin main
```

**Se pedir usuário e senha:**
- Usuário: seu username do GitHub
- Senha: **Personal Access Token** (não a senha normal!)

**Como criar Personal Access Token:**
1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token (classic)
3. Nome: "TCC Confeitaria"
4. Selecionar: `repo` (todos)
5. Generate token
6. **COPIAR E SALVAR** (não mostra de novo!)
7. Usar esse token como senha no Git

---

### **Etapa 6: Verificar no GitHub** (1 minuto)

1. Abra: `https://github.com/SEU-USUARIO/confeitaria-distribuida-tcc`
2. ✅ Deve aparecer todos os arquivos
3. ✅ README.md renderizado na página inicial
4. ✅ Documentação visível

---

## 📝 Comandos Git Úteis

### **Fazer alterações e atualizar:**

```powershell
# 1. Modificar arquivos no projeto

# 2. Ver o que mudou
git status

# 3. Adicionar mudanças
git add .

# 4. Commitar com mensagem descritiva
git commit -m "docs: Atualizar documentação de testes"

# 5. Enviar para GitHub
git push
```

### **Ver histórico:**

```powershell
# Ver todos os commits
git log

# Ver resumido
git log --oneline

# Ver últimos 5
git log -5
```

### **Voltar versão anterior (se errar):**

```powershell
# Ver commits
git log --oneline

# Voltar para commit específico (copiar hash)
git checkout abc1234

# Voltar para versão mais recente
git checkout main
```

---

## 🎯 Boas Práticas para o TCC

### **1. README.md Completo**

Deve ter:
- ✅ Título do projeto
- ✅ Descrição breve
- ✅ Como instalar e executar
- ✅ Tecnologias utilizadas
- ✅ Estrutura do projeto
- ✅ Screenshots (opcional)

### **2. Commits com Mensagens Claras**

**❌ Ruim:**
```
git commit -m "arrumei"
git commit -m "teste"
git commit -m "aaa"
```

**✅ Bom:**
```
git commit -m "feat: Adicionar endpoint de busca por categoria"
git commit -m "fix: Corrigir erro de conexão com Redis"
git commit -m "docs: Atualizar guia de instalação"
git commit -m "test: Adicionar testes de concorrência"
```

**Prefixos recomendados:**
- `feat:` - Nova funcionalidade
- `fix:` - Correção de bug
- `docs:` - Documentação
- `test:` - Testes
- `refactor:` - Refatoração
- `style:` - Formatação
- `chore:` - Tarefas gerais

### **3. Organização de Arquivos**

```
confeitaria-distribuida-tcc/
├── README.md                    ← Primeira coisa que aparece
├── .gitignore                   ← Arquivos a ignorar
├── docker-compose.yml           ← Orquestração
├── requirements.txt             ← Dependências Django
├── microservices/               ← Código dos microserviços
│   ├── catalogo/
│   └── carrinho/
├── docs/                        ← Documentação
│   ├── RELATORIO_TEMPLATE.md
│   ├── arquitetura.png
│   └── resultados/
├── confeitaria/                 ← App Django
├── pedidos/                     ← App Django
└── templates/                   ← Templates HTML
```

### **4. Documentação Visual**

Incluir no repositório:
- ✅ Diagramas de arquitetura (PNG/SVG)
- ✅ Screenshots do sistema funcionando
- ✅ Gráficos de resultados de testes
- ✅ Vídeo de demonstração (link YouTube)

---

## 📊 O que a Banca Avalia no Repositório

### **Checklist de Avaliação (30% da nota):**

| Critério | Peso | Como Melhorar |
|----------|------|---------------|
| **Organização** | 25% | Estrutura clara, arquivos bem nomeados |
| **README completo** | 20% | Instruções claras de instalação/execução |
| **Commits descritivos** | 15% | Mensagens claras, commits frequentes |
| **Documentação** | 20% | Docs/ completo, diagramas, comentários no código |
| **Código funcionando** | 20% | Sem erros, dependências corretas |

### **Dicas para Impressionar:**

1. ✅ **README com badges:**
```markdown
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)
![Docker](https://img.shields.io/badge/Docker-24.0-blue)
```

2. ✅ **Diagrama de arquitetura:**
   - Desenhar no draw.io ou Lucidchart
   - Salvar como PNG em `docs/arquitetura.png`
   - Incluir no README

3. ✅ **LICENSE:**
```markdown
MIT License

Copyright (c) 2025 Paulo Silva

Permission is hereby granted...
```

4. ✅ **CONTRIBUTING.md** (opcional)
```markdown
# Como Contribuir

Este é um projeto acadêmico (TCC).
Para reportar bugs, abra uma Issue.
```

---

## 🔗 Links Importantes

### **Seu Repositório:**
```
https://github.com/SEU-USUARIO/confeitaria-distribuida-tcc
```

### **Como citar no Relatório:**
```
SILVA, Paulo. Sistema Distribuído de E-commerce para Confeitaria.
2025. Disponível em: <https://github.com/SEU-USUARIO/confeitaria-distribuida-tcc>.
Acesso em: 18 out. 2025.
```

### **Exemplo de README para copiar:**
```markdown
# 🍰 Sistema Distribuído de E-commerce para Confeitaria

Sistema de marketplace distribuído desenvolvido como TCC da disciplina
Sistemas Distribuídos e Aplicações em Nuvem.

## 🎯 Descrição

E-commerce com arquitetura de microserviços para demonstrar conceitos de
sistemas distribuídos: transparência, escalabilidade, replicação e tolerância a falhas.

## 🏗️ Arquitetura

- **Catálogo Service**: Gerenciamento de produtos (Flask + PostgreSQL)
- **Carrinho Service**: Carrinho de compras com sessões (Flask + Redis)
- **PostgreSQL Master-Slave**: Replicação de dados
- **Docker Compose**: Orquestração de containers

## 🚀 Como Executar

### Pré-requisitos
- Docker Desktop 24.0+
- Docker Compose 2.0+

### Passos
\`\`\`bash
# 1. Clonar repositório
git clone https://github.com/SEU-USUARIO/confeitaria-distribuida-tcc.git
cd confeitaria-distribuida-tcc

# 2. Subir containers
docker-compose up -d

# 3. Popular banco de dados
docker exec -it catalogo-service python seed_data.py

# 4. Acessar APIs
# Catálogo: http://localhost:5001/api/produtos
# Carrinho: http://localhost:5002/api/carrinho
\`\`\`

## 📚 Documentação

- [Arquitetura Detalhada](ARQUITETURA_DISTRIBUIDA.md)
- [Guia de Execução](GUIA_EXECUCAO.md)
- [Testes Práticos](TESTES_PRATICOS.md)
- [Relatório Técnico](docs/RELATORIO_TEMPLATE.md)

## 🛠️ Tecnologias

- Python 3.11
- Flask 3.0
- PostgreSQL 15
- Redis 7
- Docker & Docker Compose

## 👥 Autores

- Paulo Silva - R.A. 123456

## 📄 Licença

MIT License - Projeto Acadêmico TCC
\`\`\`

---

## ✅ Checklist Final

Antes de apresentar o TCC:

- [ ] Código completo no GitHub
- [ ] README.md bem escrito
- [ ] .gitignore configurado
- [ ] Commits com mensagens claras
- [ ] Documentação completa
- [ ] Link do repositório no relatório
- [ ] Repositório público (banca pode acessar)
- [ ] Screenshots/diagramas incluídos
- [ ] Instruções de execução testadas

---

## 🆘 Problemas Comuns

### **Erro: "fatal: remote origin already exists"**
```powershell
# Remover remote antigo
git remote remove origin

# Adicionar novo
git remote add origin https://github.com/SEU-USUARIO/confeitaria-distribuida-tcc.git
```

### **Erro: "Updates were rejected"**
```powershell
# Forçar push (cuidado!)
git push -f origin main
```

### **Senha não aceita**
- Usar Personal Access Token, não senha normal
- Configurar: Settings → Developer settings → Personal access tokens

### **Arquivos muito grandes**
```powershell
# Ver tamanho dos arquivos
git ls-files | xargs ls -lh

# Remover arquivo grande do histórico
git rm --cached arquivo-grande.zip
git commit -m "Remove arquivo grande"
```

---

**Pronto para criar seu repositório?** Digite no terminal:

```powershell
cd "C:\Users\PauloH\Documents\trabalho confeitaria\confeitaria-main"
git init
git status
```

E me avise o que apareceu! 🚀
