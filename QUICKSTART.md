# 🚗 MechFinder - Guia Rápido de Instalação

## ⚡ INSTALAÇÃO RÁPIDA (3 PASSOS)

### 1️⃣ Instalar Python
- Baixe: https://www.python.org/downloads/
- Durante instalação: ✅ Marque "Add Python to PATH"

### 2️⃣ Executar Instalação Automática
```powershell
python install.py
```

### 3️⃣ Executar Aplicação
```powershell
python run.py
```

**Pronto! Acesse:** http://localhost:5000

---

## 📋 REQUISITOS

- **Python 3.8+** (recomendado: Python 3.10+)
- **5 GB de espaço** (para dependências)
- **Conexão com internet** (primeira instalação)

---

## 🔧 INSTALAÇÃO MANUAL (SE PREFERIR)

```powershell
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Criar banco de dados
python setup_db.py
python migrate_db.py
python migrate_image_search.py

# 3. Executar
python run.py
```

---

## 🌐 ACESSAR DE OUTROS DISPOSITIVOS

### Descobrir seu IP:
```powershell
ipconfig
```

### Acessar de outro dispositivo (mesma rede):
```
http://SEU_IP:5000
```

**Exemplo:** `http://192.168.1.100:5000`

---

## 📱 FUNCIONALIDADES

- ✅ Busca por texto
- ✅ **Busca por imagem com IA** (câmera ou upload)
- ✅ Geolocalização de lojas
- ✅ Carrinho de compras
- ✅ Gráficos analíticos
- ✅ Relatórios PDF
- ✅ Contato direto (WhatsApp, Tel, Email)

---

## 🐛 PROBLEMAS?

### "Python não é reconhecido"
➡️ Reinstale Python marcando "Add to PATH"

### "Erro ao instalar dependências"
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### "Porta 5000 em uso"
➡️ Altere a porta em `run.py` (linha 6):
```python
app.run(host='0.0.0.0', port=5001, debug=True)
```

---

## 📚 DOCUMENTAÇÃO COMPLETA

- `INSTALLATION_GUIDE.md` - Guia detalhado de instalação
- `README.md` - Documentação completa do projeto
- `IMAGE_SEARCH_GUIDE.md` - Guia de busca por imagem
- `VALIDATION_COMPLETE.md` - Validação e testes

---

## 🎯 PRÓXIMOS PASSOS

1. Execute `python install.py`
2. Execute `python run.py`
3. Acesse `http://localhost:5000`
4. Registre-se como usuário
5. Explore as funcionalidades!

---

**Desenvolvido com Flask, Python, IA (ResNet50) e muito ☕**

**MechFinder © 2024 - Sistema de Busca Automotiva Inteligente 🚗✨**
