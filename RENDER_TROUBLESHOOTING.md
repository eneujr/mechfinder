# 🐛 TROUBLESHOOTING - RENDER DEPLOY

## ❌ ERRO: ModuleNotFoundError: No module named 'your_application'

### 🔍 CAUSA:

Este erro acontece quando:
1. O **Start Command** está incorreto no Render
2. O **Procfile** não está sendo lido
3. Estrutura de arquivos está incorreta

---

## ✅ SOLUÇÃO PASSO A PASSO

### **SOLUÇÃO 1: VERIFICAR START COMMAND NO RENDER**

#### **Passo 1: Acessar Configurações**

1. Acesse: https://dashboard.render.com
2. Clique no seu Web Service (`mechfinder`)
3. Vá em **Settings** (menu lateral)

#### **Passo 2: Verificar Start Command**

Role até **Build & Deploy**

**Start Command deve ser EXATAMENTE:**
```
gunicorn run:app
```

**NÃO deve ser:**
- ❌ `gunicorn your_application:app`
- ❌ `gunicorn app:app`
- ❌ `python run.py`

#### **Passo 3: Salvar e Redeploy**

1. Se estava errado, corrija para: `gunicorn run:app`
2. Clique **"Save Changes"**
3. Vá em **Manual Deploy** → **"Deploy latest commit"**

---

### **SOLUÇÃO 2: VERIFICAR ESTRUTURA DE ARQUIVOS**

#### **Estrutura Correta:**

```
chrono-planck/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes/
│   ├── templates/
│   └── static/
├── run.py          ← IMPORTANTE!
├── Procfile        ← IMPORTANTE!
├── requirements.txt
├── runtime.txt
└── config.py
```

#### **Verificar Arquivos:**

**1. `run.py` deve conter:**
```python
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

**2. `Procfile` deve conter:**
```
web: gunicorn run:app
```

**3. `requirements.txt` deve incluir:**
```
gunicorn
```

---

### **SOLUÇÃO 3: RECRIAR WEB SERVICE**

Se as soluções acima não funcionarem:

#### **Passo 1: Deletar Service Atual**

1. Render Dashboard → Seu service
2. Settings → **Delete Web Service**
3. Confirme

#### **Passo 2: Criar Novo Service**

1. **New +** → **Web Service**
2. Connect repository `mechfinder`
3. **Configure CORRETAMENTE:**

**Name:**
```
mechfinder
```

**Build Command:**
```
pip install -r requirements.txt
```

**Start Command:**
```
gunicorn run:app
```

**Environment Variables:**
```
SECRET_KEY = mechfinder-secret-key-12345
```

4. **Create Web Service**

---

### **SOLUÇÃO 4: VERIFICAR LOGS**

#### **Ver Logs Detalhados:**

1. Render Dashboard → Seu service
2. **Logs** (menu lateral)
3. Procure por erros específicos

**Erros Comuns:**

**Erro 1: "No module named 'app'"**
```
Solução: Verifique se pasta 'app' existe e tem __init__.py
```

**Erro 2: "No module named 'gunicorn'"**
```
Solução: Adicione 'gunicorn' ao requirements.txt
```

**Erro 3: "Application failed to start"**
```
Solução: Verifique SECRET_KEY nas environment variables
```

---

## 🔧 VERIFICAÇÃO COMPLETA

### **Checklist de Arquivos:**

Execute localmente para verificar:

```powershell
# 1. Verificar estrutura
dir

# Deve mostrar:
# - app (pasta)
# - run.py
# - Procfile
# - requirements.txt
# - runtime.txt

# 2. Verificar conteúdo do Procfile
type Procfile

# Deve mostrar:
# web: gunicorn run:app

# 3. Verificar requirements.txt
type requirements.txt | findstr gunicorn

# Deve mostrar:
# gunicorn

# 4. Testar localmente
pip install gunicorn
gunicorn run:app

# Se funcionar localmente, deve funcionar no Render
```

---

## 📝 CONFIGURAÇÃO CORRETA DO RENDER

### **Settings → Build & Deploy:**

```yaml
Build Command:
  pip install -r requirements.txt

Start Command:
  gunicorn run:app
```

### **Settings → Environment:**

```
SECRET_KEY = sua-chave-secreta-aqui
PYTHON_VERSION = 3.10.12
```

---

## 🚀 SOLUÇÃO RÁPIDA (COPIAR E COLAR)

### **Se tudo mais falhar, recrie os arquivos:**

#### **1. Criar novo `Procfile`:**

```powershell
echo web: gunicorn run:app > Procfile
```

#### **2. Verificar `run.py`:**

Deve ter exatamente:
```python
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

#### **3. Commit e Push:**

```powershell
git add Procfile run.py
git commit -m "Fix: Corrigir Procfile e run.py"
git push
```

#### **4. Redeploy no Render:**

1. Render Dashboard
2. Manual Deploy → Deploy latest commit

---

## 🎯 TESTE LOCAL ANTES DE DEPLOY

### **Testar com Gunicorn localmente:**

```powershell
# 1. Instalar gunicorn
pip install gunicorn

# 2. Testar
gunicorn run:app

# 3. Acessar
# http://localhost:8000

# Se funcionar, Ctrl+C para parar
```

**Se funcionar localmente, funcionará no Render!**

---

## 📊 COMPARAÇÃO: CERTO vs ERRADO

| Item | ❌ ERRADO | ✅ CERTO |
|------|----------|---------|
| **Procfile** | `web: python run.py` | `web: gunicorn run:app` |
| **Start Command** | `python run.py` | `gunicorn run:app` |
| **run.py** | Não existe | Existe na raiz |
| **requirements.txt** | Sem gunicorn | Com gunicorn |

---

## 🔄 ATUALIZAR PROJETO NO GITHUB

### **Se fez mudanças:**

```powershell
# 1. Adicionar mudanças
git add .

# 2. Commit
git commit -m "Fix: Corrigir configuração para deploy"

# 3. Push
git push

# 4. Render fará deploy automático
```

---

## 💡 DICA PRO

### **Criar arquivo `render.yaml` (opcional):**

Crie na raiz do projeto:

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

Isso garante configuração correta sempre!

---

## 🎉 RESUMO DA SOLUÇÃO

### **Passo a Passo Rápido:**

1. **Render Dashboard** → Seu service → **Settings**
2. **Start Command:** `gunicorn run:app`
3. **Save Changes**
4. **Manual Deploy** → **Deploy latest commit**
5. Aguarde build
6. **Pronto!** ✅

---

## 📞 AINDA COM PROBLEMAS?

### **Envie os logs:**

1. Render → Logs
2. Copie últimas 50 linhas
3. Procure por:
   - `ModuleNotFoundError`
   - `ImportError`
   - `Application error`

### **Verifique:**

- [ ] `Procfile` existe na raiz
- [ ] `run.py` existe na raiz
- [ ] `gunicorn` está em `requirements.txt`
- [ ] Start Command é `gunicorn run:app`
- [ ] Pasta `app` existe com `__init__.py`

---

**Se seguir este guia, o erro será resolvido! 🚀**
