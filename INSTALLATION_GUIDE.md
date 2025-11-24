# 🚀 GUIA DE INSTALAÇÃO E EXECUÇÃO EM OUTRO COMPUTADOR

## 📋 PRÉ-REQUISITOS

### Software Necessário:
- **Python 3.8 ou superior** (recomendado: Python 3.10+)
- **Git** (opcional, para clonar o repositório)
- **Navegador web** moderno (Chrome, Firefox, Edge)

---

## 📦 OPÇÃO 1: TRANSFERIR ARQUIVOS MANUALMENTE

### Passo 1: Copiar Projeto

**Copie toda a pasta do projeto:**
```
chrono-planck/
```

**Métodos de transferência:**
- Pendrive/HD externo
- Compartilhamento de rede
- Compactar em ZIP e enviar por email/nuvem
- GitHub (recomendado)

### Passo 2: No Novo Computador

1. **Cole a pasta** em um local de sua escolha
   Exemplo: `C:\Projetos\chrono-planck`

2. **Abra o PowerShell** nessa pasta
   - Clique com botão direito na pasta
   - Escolha "Abrir no Terminal" ou "PowerShell aqui"

---

## 🔧 OPÇÃO 2: USAR GITHUB (RECOMENDADO)

### No Computador Original:

```powershell
# 1. Inicializar repositório Git (se ainda não fez)
cd C:\Users\eneuj\.gemini\antigravity\playground\chrono-planck
git init

# 2. Adicionar arquivos
git add .

# 3. Fazer commit
git commit -m "MechFinder - Sistema completo"

# 4. Criar repositório no GitHub
# Acesse: https://github.com/new
# Crie um repositório chamado "mechfinder"

# 5. Conectar e enviar
git remote add origin https://github.com/SEU_USUARIO/mechfinder.git
git branch -M main
git push -u origin main
```

### No Novo Computador:

```powershell
# 1. Clonar repositório
git clone https://github.com/SEU_USUARIO/mechfinder.git
cd mechfinder
```

---

## 🛠️ INSTALAÇÃO NO NOVO COMPUTADOR

### Passo 1: Verificar Python

```powershell
# Verificar versão do Python
python --version

# Deve mostrar: Python 3.8.x ou superior
```

**Se não tiver Python:**
- Baixe em: https://www.python.org/downloads/
- Durante instalação, marque "Add Python to PATH"

### Passo 2: Criar Ambiente Virtual (Recomendado)

```powershell
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows:
.\venv\Scripts\Activate

# Linux/Mac:
source venv/bin/activate
```

### Passo 3: Instalar Dependências

```powershell
# Instalar todas as dependências
pip install -r requirements.txt

# ⚠️ ATENÇÃO: Primeira instalação pode demorar 5-10 minutos
# (download do PyTorch e outras bibliotecas grandes)
```

**Se der erro de instalação:**
```powershell
# Atualizar pip primeiro
python -m pip install --upgrade pip

# Tentar novamente
pip install -r requirements.txt
```

### Passo 4: Configurar Banco de Dados

```powershell
# Criar banco de dados
python setup_db.py

# Aplicar migrações
python migrate_db.py
python migrate_image_search.py
```

### Passo 5: Executar Aplicação

```powershell
# Iniciar servidor
python run.py
```

**Você verá:**
```
* Running on http://0.0.0.0:5000
* Running on http://192.168.X.X:5000
```

### Passo 6: Acessar no Navegador

```
http://localhost:5000
```

---

## 🌐 ACESSAR DE OUTROS DISPOSITIVOS NA MESMA REDE

### Descobrir IP do Computador:

**Windows:**
```powershell
ipconfig
# Procure por "IPv4 Address"
# Exemplo: 192.168.1.100
```

**Linux/Mac:**
```bash
ifconfig
# ou
ip addr show
```

### Acessar de Outro Dispositivo:

```
http://192.168.X.X:5000
```

**Exemplo:**
```
http://192.168.1.100:5000
```

### Liberar Firewall (Windows):

```powershell
# Executar PowerShell como Administrador
netsh advfirewall firewall add rule name="Flask MechFinder" dir=in action=allow protocol=TCP localport=5000
```

---

## 📱 OPÇÃO 3: DEPLOY EM NUVEM (ACESSO DE QUALQUER LUGAR)

### A. Render (Gratuito)

1. **Criar conta:** https://render.com
2. **Criar Web Service:**
   - Conectar GitHub
   - Selecionar repositório
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn run:app`
3. **Adicionar ao requirements.txt:**
   ```
   gunicorn
   ```

### B. Heroku (Gratuito com limitações)

1. **Criar conta:** https://heroku.com
2. **Instalar Heroku CLI**
3. **Deploy:**
   ```powershell
   heroku login
   heroku create mechfinder-app
   git push heroku main
   ```

### C. PythonAnywhere (Gratuito)

1. **Criar conta:** https://www.pythonanywhere.com
2. **Upload de arquivos**
3. **Configurar Web App**
4. **Acessar:** `seu-usuario.pythonanywhere.com`

---

## 📝 CHECKLIST DE INSTALAÇÃO

### No Novo Computador:

- [ ] Python 3.8+ instalado
- [ ] Projeto copiado/clonado
- [ ] Ambiente virtual criado (opcional mas recomendado)
- [ ] Dependências instaladas (`pip install -r requirements.txt`)
- [ ] Banco de dados criado (`python setup_db.py`)
- [ ] Migrações aplicadas
- [ ] Servidor rodando (`python run.py`)
- [ ] Acesso funcionando (`http://localhost:5000`)

---

## 🐛 TROUBLESHOOTING

### Erro: "Python não é reconhecido"
**Solução:** Adicionar Python ao PATH
- Reinstalar Python marcando "Add to PATH"
- Ou adicionar manualmente nas variáveis de ambiente

### Erro: "pip não encontrado"
**Solução:**
```powershell
python -m ensurepip --upgrade
python -m pip install --upgrade pip
```

### Erro: "ModuleNotFoundError"
**Solução:**
```powershell
# Reinstalar dependências
pip install -r requirements.txt --force-reinstall
```

### Erro: "Porta 5000 já em uso"
**Solução:** Alterar porta em `run.py`:
```python
app.run(host='0.0.0.0', port=5001, debug=True)
```

### Erro: "Banco de dados não encontrado"
**Solução:**
```powershell
# Recriar banco
python setup_db.py
python migrate_db.py
python migrate_image_search.py
```

### Erro ao instalar PyTorch (muito grande)
**Solução:** Instalar versão CPU-only (menor):
```powershell
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

---

## 📊 COMPARAÇÃO DE OPÇÕES

| Opção | Vantagens | Desvantagens |
|-------|-----------|--------------|
| **Local** | Rápido, sem custo | Apenas no computador |
| **Rede Local** | Acesso na mesma rede | Precisa estar conectado |
| **Render** | Gratuito, fácil | Pode dormir após inatividade |
| **Heroku** | Confiável | Limite de horas gratuitas |
| **PythonAnywhere** | Simples | Recursos limitados |

---

## 🎯 RECOMENDAÇÕES

### Para Desenvolvimento:
✅ **Executar localmente** com ambiente virtual

### Para Demonstração:
✅ **Rede local** (mesma WiFi)

### Para Produção:
✅ **Deploy em nuvem** (Render ou Heroku)

---

## 📦 ESTRUTURA DE ARQUIVOS NECESSÁRIOS

```
chrono-planck/
├── app/                    # Código da aplicação
├── instance/               # Banco de dados (será criado)
├── requirements.txt        # Dependências
├── run.py                  # Arquivo principal
├── setup_db.py            # Script de criação do banco
├── migrate_db.py          # Migração
├── migrate_image_search.py # Migração de busca por imagem
└── README.md              # Documentação
```

**Arquivos que NÃO precisam ser copiados:**
- `venv/` (ambiente virtual - será criado no novo PC)
- `__pycache__/` (cache do Python)
- `.pyc` (arquivos compilados)

---

## 🚀 COMANDOS RÁPIDOS

### Instalação Completa (Novo PC):

```powershell
# 1. Criar ambiente virtual
python -m venv venv
.\venv\Scripts\Activate

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Configurar banco
python setup_db.py
python migrate_db.py
python migrate_image_search.py

# 4. Executar
python run.py
```

### Acesso:
```
Local: http://localhost:5000
Rede: http://SEU_IP:5000
```

---

## 📞 SUPORTE

### Documentação:
- `README.md` - Visão geral
- `IMAGE_SEARCH_GUIDE.md` - Busca por imagem
- `IMAGE_SEARCH_IMPROVEMENTS.md` - Melhorias
- `VALIDATION_COMPLETE.md` - Validação

### Logs de Erro:
- Verifique o terminal onde executou `python run.py`
- Pressione F12 no navegador para ver erros JavaScript

---

## 🎉 CONCLUSÃO

**Opção Mais Simples:**
1. Copiar pasta do projeto
2. Instalar Python
3. `pip install -r requirements.txt`
4. `python setup_db.py`
5. `python run.py`

**Pronto! Aplicação rodando! 🚗✨**
