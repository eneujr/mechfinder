# 🔧 INSTALAR E CONFIGURAR GIT NO WINDOWS

## ❌ PROBLEMA: "git não é reconhecido"

Isso significa que o Git não está instalado ou não está no PATH do sistema.

---

## ✅ SOLUÇÃO: INSTALAR GIT

### **OPÇÃO 1: INSTALAÇÃO RÁPIDA (RECOMENDADO)**

#### **Passo 1: Baixar Git**

1. Acesse: https://git-scm.com/download/win
2. Download automático começará
3. Ou clique em: **"Click here to download manually"**
4. Escolha: **"64-bit Git for Windows Setup"**

#### **Passo 2: Instalar**

1. Execute o arquivo baixado (`Git-2.x.x-64-bit.exe`)
2. **Configurações recomendadas:**

**Tela 1 - Select Components:**
- ✅ Marque tudo (padrão está OK)

**Tela 2 - Choosing the default editor:**
- Escolha: **"Use Notepad as Git's default editor"** (mais simples)

**Tela 3 - Adjusting your PATH environment:**
- ✅ **"Git from the command line and also from 3rd-party software"** (IMPORTANTE!)

**Tela 4 - Choosing HTTPS transport backend:**
- ✅ "Use the OpenSSL library" (padrão)

**Demais telas:**
- Deixe padrão e clique "Next"

3. Clique **"Install"**
4. Aguarde instalação
5. Clique **"Finish"**

#### **Passo 3: Verificar Instalação**

1. **Feche o PowerShell** (importante!)
2. **Abra novo PowerShell**
3. Digite:

```powershell
git --version
```

**Deve mostrar:**
```
git version 2.x.x
```

✅ **Git instalado com sucesso!**

---

### **OPÇÃO 2: USAR GITHUB DESKTOP (MAIS FÁCIL)**

Se preferir interface gráfica:

#### **Passo 1: Baixar GitHub Desktop**

1. Acesse: https://desktop.github.com
2. Clique "Download for Windows"
3. Execute o instalador

#### **Passo 2: Configurar**

1. Abra GitHub Desktop
2. Faça login com sua conta GitHub
3. Pronto!

#### **Passo 3: Adicionar Projeto**

1. File → Add Local Repository
2. Escolha a pasta: `C:\Users\eneuj\.gemini\antigravity\playground\chrono-planck`
3. Ou: File → New Repository (se ainda não tem Git)

#### **Passo 4: Commit e Push**

1. Escreva mensagem: "Deploy inicial"
2. Clique "Commit to main"
3. Clique "Publish repository"
4. Escolha nome: `mechfinder`
5. Clique "Publish repository"

✅ **Projeto no GitHub!**

---

## 🔧 CONFIGURAR GIT (PRIMEIRA VEZ)

Depois de instalar, configure:

```powershell
# Seu nome
git config --global user.name "Seu Nome Aqui"

# Seu email (mesmo do GitHub)
git config --global user.email "seu@email.com"

# Verificar configuração
git config --list
```

---

## 📋 COMANDOS COMPLETOS APÓS INSTALAR

### **Passo a Passo:**

```powershell
# 1. Navegar até a pasta
cd C:\Users\eneuj\.gemini\antigravity\playground\chrono-planck

# 2. Verificar Git
git --version

# 3. Configurar (primeira vez)
git config --global user.name "Seu Nome"
git config --global user.email "seu@email.com"

# 4. Inicializar repositório
git init

# 5. Adicionar arquivos
git add .

# 6. Fazer commit
git commit -m "MechFinder - Deploy inicial"

# 7. Conectar ao GitHub (substitua SEU_USUARIO)
git remote add origin https://github.com/SEU_USUARIO/mechfinder.git

# 8. Renomear branch
git branch -M main

# 9. Enviar para GitHub
git push -u origin main
```

---

## 🐛 TROUBLESHOOTING

### **Problema 1: "git ainda não é reconhecido"**

**Solução:**
1. Feche TODOS os PowerShells abertos
2. Abra NOVO PowerShell
3. Tente novamente

**Se ainda não funcionar:**
1. Reinicie o computador
2. Abra PowerShell
3. Tente novamente

### **Problema 2: "Permission denied (publickey)"**

**Solução:** Use HTTPS ao invés de SSH

```powershell
# URL correta (HTTPS):
git remote add origin https://github.com/SEU_USUARIO/mechfinder.git

# NÃO use (SSH):
# git remote add origin git@github.com:SEU_USUARIO/mechfinder.git
```

### **Problema 3: "Authentication failed"**

**Solução:** Use Personal Access Token

1. GitHub → Settings → Developer settings
2. Personal access tokens → Tokens (classic)
3. Generate new token (classic)
4. Nome: "MechFinder Deploy"
5. Marque: ✅ `repo` (full control)
6. Generate token
7. **COPIE O TOKEN** (não vai aparecer de novo!)
8. Use como senha no `git push`

---

## 🎯 ALTERNATIVA: USAR GITHUB.COM (SEM GIT)

Se não quiser instalar Git, use interface web:

### **Passo 1: Criar Repositório**

1. GitHub → New repository
2. Nome: `mechfinder`
3. Create repository

### **Passo 2: Upload Manual**

1. No repositório criado, clique "uploading an existing file"
2. Arraste TODOS os arquivos da pasta `chrono-planck`
3. Commit message: "Initial commit"
4. Commit changes

**Desvantagem:** Precisa fazer upload manual toda vez que atualizar

---

## 📊 COMPARAÇÃO DE OPÇÕES

| Método | Facilidade | Recomendado |
|--------|------------|-------------|
| **Git CLI** | ⭐⭐⭐ | Profissional |
| **GitHub Desktop** | ⭐⭐⭐⭐⭐ | **SIM!** ⭐ |
| **Upload Web** | ⭐⭐⭐⭐ | Iniciante |

---

## 🚀 RECOMENDAÇÃO

### **Para você:**

**Use GitHub Desktop!**

**Por quê?**
- ✅ Mais fácil (interface gráfica)
- ✅ Não precisa decorar comandos
- ✅ Vê mudanças visualmente
- ✅ Commit e push com 2 cliques

**Como:**
1. Baixe: https://desktop.github.com
2. Instale
3. Faça login
4. Add Local Repository
5. Commit
6. Publish

**Pronto em 5 minutos!**

---

## 📝 RESUMO RÁPIDO

### **Opção 1 - Git CLI:**
```powershell
# Baixe: https://git-scm.com/download/win
# Instale
# Feche e abra novo PowerShell
git --version
# Configure e use
```

### **Opção 2 - GitHub Desktop (RECOMENDADO):**
```
1. Baixe: https://desktop.github.com
2. Instale
3. Faça login
4. Add repository
5. Commit → Publish
6. Pronto!
```

### **Opção 3 - Upload Web:**
```
1. GitHub → New repository
2. Upload files
3. Commit
4. Pronto!
```

---

## 🎉 PRÓXIMOS PASSOS

**Depois de enviar para GitHub:**

1. Acesse Render: https://render.com
2. New Web Service
3. Connect GitHub
4. Selecione `mechfinder`
5. Deploy!

**Guia completo:** `RENDER_DEPLOY_GUIDE.md`

---

## 📞 LINKS ÚTEIS

- **Git Download:** https://git-scm.com/download/win
- **GitHub Desktop:** https://desktop.github.com
- **GitHub:** https://github.com
- **Render:** https://render.com

---

**Escolha a opção que preferir e siga em frente! 🚀**
