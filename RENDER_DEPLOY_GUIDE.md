# 🚀 DEPLOY NO RENDER - GUIA PASSO A PASSO COMPLETO

## 📋 VISÃO GERAL

Este guia mostra como fazer deploy do MechFinder no Render (gratuito) conectando ao GitHub.

**Tempo estimado:** 15-20 minutos

---

## PARTE 1: PREPARAR PROJETO PARA DEPLOY

### Passo 1: Criar Arquivos Necessários

#### 1.1 Criar `Procfile` (para Render)

No diretório do projeto, crie o arquivo `Procfile`:

```
web: gunicorn run:app
```

#### 1.2 Criar `runtime.txt` (versão do Python)

```
python-3.10.12
```

#### 1.3 Atualizar `requirements.txt`

Adicione `gunicorn` ao final:

```
Flask
Flask-SQLAlchemy
Flask-Login
Flask-WTF
email_validator
reportlab
Werkzeug
Pillow
torch
torchvision
numpy
scikit-learn
gunicorn
```

#### 1.4 Criar `render.yaml` (opcional, mas recomendado)

```yaml
services:
  - type: web
    name: mechfinder
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn run:app
    envVars:
      - key: PYTHON_VERSION
        value: 3.10.12
      - key: SECRET_KEY
        generateValue: true
```

---

## PARTE 2: ENVIAR PROJETO PARA GITHUB

### Passo 2: Criar Repositório no GitHub

#### 2.1 Acessar GitHub

1. Abra: https://github.com
2. Faça login (ou crie conta se não tiver)

#### 2.2 Criar Novo Repositório

1. Clique no **"+"** no canto superior direito
2. Selecione **"New repository"**
3. Preencha:
   - **Repository name:** `mechfinder`
   - **Description:** "Sistema de Busca Automotiva Inteligente"
   - **Visibility:** Public (ou Private se preferir)
   - ❌ **NÃO marque** "Add a README file"
   - ❌ **NÃO marque** "Add .gitignore"
4. Clique em **"Create repository"**

#### 2.3 Copiar URL do Repositório

Você verá uma URL como:
```
https://github.com/SEU_USUARIO/mechfinder.git
```

**Guarde essa URL!**

---

### Passo 3: Configurar Git no Seu Computador

#### 3.1 Verificar se Git está instalado

```powershell
git --version
```

**Se não tiver Git:**
- Baixe: https://git-scm.com/download/win
- Instale com configurações padrão

#### 3.2 Configurar Git (primeira vez)

```powershell
git config --global user.name "Seu Nome"
git config --global user.email "seu@email.com"
```

---

### Passo 4: Enviar Projeto para GitHub

#### 4.1 Abrir PowerShell na pasta do projeto

```powershell
cd C:\Users\eneuj\.gemini\antigravity\playground\chrono-planck
```

#### 4.2 Criar `.gitignore`

Crie arquivo `.gitignore` com este conteúdo:

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# Flask
instance/
.webassets-cache

# Database
*.db
*.sqlite
*.sqlite3

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Uploads (opcional - comente se quiser enviar imagens)
app/static/uploads/*
!app/static/uploads/.gitkeep
```

#### 4.3 Inicializar Git

```powershell
git init
```

#### 4.4 Adicionar arquivos

```powershell
git add .
```

#### 4.5 Fazer primeiro commit

```powershell
git commit -m "Initial commit - MechFinder completo"
```

#### 4.6 Conectar ao GitHub

```powershell
# Substitua SEU_USUARIO pelo seu usuário do GitHub
git remote add origin https://github.com/SEU_USUARIO/mechfinder.git
```

#### 4.7 Renomear branch para main

```powershell
git branch -M main
```

#### 4.8 Enviar para GitHub

```powershell
git push -u origin main
```

**Vai pedir login:**
- Username: seu usuário do GitHub
- Password: use um **Personal Access Token** (não a senha)

**Como criar Personal Access Token:**
1. GitHub → Settings → Developer settings
2. Personal access tokens → Tokens (classic)
3. Generate new token
4. Marque: `repo` (full control)
5. Copie o token gerado
6. Use como senha no git push

---

## PARTE 3: DEPLOY NO RENDER

### Passo 5: Criar Conta no Render

#### 5.1 Acessar Render

1. Abra: https://render.com
2. Clique em **"Get Started"**

#### 5.2 Criar Conta

**Opção 1 - Com GitHub (Recomendado):**
1. Clique em **"Sign up with GitHub"**
2. Autorize o Render

**Opção 2 - Com Email:**
1. Preencha email e senha
2. Confirme email

---

### Passo 6: Criar Web Service

#### 6.1 Novo Web Service

1. No dashboard do Render, clique em **"New +"**
2. Selecione **"Web Service"**

#### 6.2 Conectar Repositório

1. Se ainda não conectou GitHub:
   - Clique em **"Connect GitHub"**
   - Autorize o Render
   
2. Encontre seu repositório:
   - Procure por `mechfinder`
   - Clique em **"Connect"**

#### 6.3 Configurar Service

Preencha os campos:

**Name:**
```
mechfinder
```

**Region:**
```
Oregon (US West) - ou o mais próximo
```

**Branch:**
```
main
```

**Root Directory:**
```
(deixe em branco)
```

**Runtime:**
```
Python 3
```

**Build Command:**
```
pip install -r requirements.txt
```

**Start Command:**
```
gunicorn run:app
```

#### 6.4 Configurar Plano

1. Selecione **"Free"** (gratuito)
2. Clique em **"Advanced"** para mais opções

#### 6.5 Variáveis de Ambiente

Clique em **"Add Environment Variable"**

Adicione:

**SECRET_KEY:**
```
Key: SECRET_KEY
Value: sua-chave-secreta-aqui-123456789
```

**PYTHON_VERSION:**
```
Key: PYTHON_VERSION
Value: 3.10.12
```

#### 6.6 Criar Web Service

1. Revise as configurações
2. Clique em **"Create Web Service"**

---

### Passo 7: Aguardar Deploy

#### 7.1 Acompanhar Build

Você verá logs em tempo real:

```
Building...
Installing dependencies...
Starting application...
```

**Tempo estimado:** 5-10 minutos (primeira vez)

#### 7.2 Deploy Completo

Quando ver:
```
✓ Build successful
✓ Deploy live
```

Seu app está no ar! 🎉

---

### Passo 8: Acessar Aplicação

#### 8.1 Obter URL

Render gera uma URL automática:
```
https://mechfinder.onrender.com
```

#### 8.2 Testar

1. Clique na URL
2. Aguarde carregar (primeira vez pode demorar)
3. Faça login/registro
4. Teste funcionalidades!

---

## PARTE 4: CONFIGURAÇÕES ADICIONAIS

### Passo 9: Configurar Banco de Dados (Opcional)

**Render Free usa disco efêmero** (dados são perdidos ao reiniciar)

**Para banco persistente:**

#### 9.1 Adicionar PostgreSQL

1. No Render Dashboard: **"New +"** → **"PostgreSQL"**
2. Configure:
   - Name: `mechfinder-db`
   - Plan: Free
3. Clique em **"Create Database"**

#### 9.2 Conectar ao Web Service

1. Copie **Internal Database URL**
2. No Web Service → **Environment**
3. Adicione variável:
   ```
   Key: DATABASE_URL
   Value: [cole a URL do PostgreSQL]
   ```

#### 9.3 Atualizar `config.py`

```python
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    
    # Usar PostgreSQL se disponível, senão SQLite
    DATABASE_URL = os.environ.get('DATABASE_URL')
    if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
    
    SQLALCHEMY_DATABASE_URI = DATABASE_URL or \
        'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance', 'mechfinder.db')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'app/static/uploads'
```

---

### Passo 10: Domínio Personalizado (Opcional)

#### 10.1 Adicionar Domínio

1. No Web Service → **Settings**
2. **Custom Domain** → **Add Custom Domain**
3. Digite seu domínio: `www.mechfinder.com.br`
4. Configure DNS conforme instruções

---

## PARTE 5: ATUALIZAÇÕES FUTURAS

### Passo 11: Como Atualizar o App

#### 11.1 Fazer Alterações Localmente

```powershell
# Edite os arquivos que quiser
```

#### 11.2 Commit e Push

```powershell
git add .
git commit -m "Descrição das mudanças"
git push
```

#### 11.3 Deploy Automático

Render detecta o push e faz deploy automaticamente! 🚀

---

## 📋 CHECKLIST COMPLETO

### Preparação:
- [ ] Criar `Procfile`
- [ ] Criar `runtime.txt`
- [ ] Adicionar `gunicorn` ao `requirements.txt`
- [ ] Criar `.gitignore`

### GitHub:
- [ ] Criar conta no GitHub
- [ ] Criar repositório `mechfinder`
- [ ] Instalar Git no PC
- [ ] Configurar Git (nome e email)
- [ ] `git init`
- [ ] `git add .`
- [ ] `git commit -m "Initial commit"`
- [ ] `git remote add origin URL`
- [ ] `git push -u origin main`

### Render:
- [ ] Criar conta no Render
- [ ] Conectar GitHub ao Render
- [ ] Criar Web Service
- [ ] Conectar repositório
- [ ] Configurar build/start commands
- [ ] Adicionar variáveis de ambiente
- [ ] Criar Web Service
- [ ] Aguardar deploy
- [ ] Testar URL gerada

---

## 🐛 TROUBLESHOOTING

### Erro: "Build failed"

**Solução:**
1. Verifique logs no Render
2. Confirme que `requirements.txt` está correto
3. Verifique `Procfile` e `runtime.txt`

### Erro: "Application error"

**Solução:**
1. Verifique variável `SECRET_KEY`
2. Veja logs: Render Dashboard → Logs
3. Confirme que `run.py` existe

### Erro: "Git push rejected"

**Solução:**
```powershell
git pull origin main --rebase
git push
```

### App muito lento

**Solução:**
- Normal no plano Free
- App "dorme" após 15min de inatividade
- Primeira requisição demora ~30s

---

## 💡 DICAS IMPORTANTES

### 1. Plano Free - Limitações:
- ✅ 750 horas/mês (suficiente)
- ⚠️ App dorme após 15min inatividade
- ⚠️ Banco de dados efêmero (dados perdidos ao reiniciar)
- ⚠️ 512MB RAM

### 2. Manter App Ativo:
Use serviço de ping (UptimeRobot):
- https://uptimerobot.com
- Ping a cada 5 minutos
- Mantém app acordado

### 3. Banco Persistente:
- Use PostgreSQL do Render (Free)
- Ou use serviço externo (ElephantSQL)

---

## 🎉 CONCLUSÃO

**Parabéns! Seu MechFinder está online! 🚗✨**

**URL:** `https://mechfinder.onrender.com`

**Próximos passos:**
1. Teste todas as funcionalidades
2. Compartilhe a URL
3. Use no celular (adicione à tela inicial)
4. Configure domínio personalizado (opcional)

---

## 📞 LINKS ÚTEIS

- **Render Dashboard:** https://dashboard.render.com
- **Render Docs:** https://render.com/docs
- **GitHub:** https://github.com
- **Git Download:** https://git-scm.com

---

**Documentação criada para MechFinder**
**Qualquer dúvida, consulte os logs no Render Dashboard!**
