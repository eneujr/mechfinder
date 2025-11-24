# 🚗 MechFinder - Plataforma de Marketplace Automotivo

## 📋 Visão Geral

MechFinder é uma plataforma web completa que conecta clientes a lojas de autopeças e prestadores de serviços automotivos. O sistema oferece funcionalidades avançadas de geolocalização, gerenciamento de produtos/serviços, análise de vendas e compras com gráficos interativos.

---

## ✨ Funcionalidades Implementadas

### 1. **Sistema de Autenticação** 🔐

- **Registro de Usuários**
  - Tipos: Cliente, Lojista, Prestador de Serviços
  - Campos: Nome, E-mail, Telefone, Senha
  - Validação de dados únicos (email, username)

- **Login/Logout**
  - Autenticação segura com Flask-Login
  - Sessões persistentes
  - Redirecionamento inteligente

- **Perfil de Usuário**
  - Visualização de dados pessoais
  - Gerenciamento de lojas (lojistas/prestadores)
  - Acesso a histórico de compras/vendas

---

### 2. **Gerenciamento de Lojas** 🏪

#### **Criar Nova Loja**
- Nome da loja
- Categoria (Auto Peças, Mecânica, Funilaria, etc.)
- Telefone e WhatsApp
- E-mail
- **Endereço Completo:**
  - CEP (com busca automática via ViaCEP)
  - Endereço (preenchido automaticamente)
  - Número
  - Coordenadas GPS (latitude/longitude)

#### **Editar Loja**
- Atualização de todos os campos
- Mapa interativo para ajustar localização
- Marcador arrastável para precisão

#### **Mapa de Geolocalização**
- Biblioteca Leaflet + OpenStreetMap
- Busca automática de endereço por CEP
- Geocodificação via Nominatim API
- Marcador arrastável
- Visualização em tempo real

#### **Ativar/Desativar Lojas**
- Controle de visibilidade
- Lojas inativas não aparecem em buscas

---

### 3. **Gerenciamento de Produtos/Serviços** 📦

#### **Cadastro de Produtos**
- Nome, Categoria, Marca
- Descrição e Especificações
- Compatibilidade
- Preço
- Upload de imagem
- Garantia, Ano
- Status (Ativo/Inativo, Em Estoque)

#### **Cadastro de Serviços**
- Nome, Categoria
- Tipo de serviço
- Descrição
- Diferenciais
- Preço
- Upload de imagem

#### **Edição**
- Atualização completa de campos
- Troca de imagens
- Ativar/Desativar

#### **Visualização**
- Apenas produtos/serviços ativos aparecem na busca
- Imagens exibidas corretamente
- Informações organizadas

---

### 4. **Página de Detalhes do Produto** 🛍️

#### **Informações do Produto**
- Nome, Categoria, Avaliação
- Preço destacado
- Imagem em alta qualidade
- Descrição completa
- Especificações técnicas
- Compatibilidade
- Diferenciais (para serviços)

#### **Card da Loja**
- Nome e avaliação
- Endereço completo (rua, número, CEP)
- **Mapa de Localização:**
  - Mapa interativo mostrando a loja
  - Marcador personalizado (ícone de loja verde)
  - Popup com informações
  - Controles de zoom
  
- **Botões de Contato:**
  - **WhatsApp:** Abre WhatsApp com mensagem pré-preenchida
  - **Telefone:** Abre discador do celular
  - **E-mail:** Abre cliente de e-mail com assunto
  - **Como Chegar:** Link direto para Google Maps com rota

#### **Ações de Compra**
- Seleção de quantidade
- **Comprar Agora (Rápido):** Adiciona ao carrinho e redireciona
- **Adicionar ao Carrinho:** Adiciona e continua navegando

---

### 5. **Busca e Filtros** 🔍

- **Busca por Texto**
  - Pesquisa em nome, descrição, especificações
  - Resultados em tempo real

- **Filtro por Categoria**
  - Auto Peças, Mecânica, Funilaria, etc.
  - Múltiplas categorias

- **Filtros Automáticos**
  - Apenas produtos ativos
  - Apenas produtos em estoque
  - Ordenação por relevância

---

### 6. **Carrinho de Compras** 🛒

- **Adicionar Produtos**
  - Quantidade personalizável
  - Validação de estoque

- **Visualizar Carrinho**
  - Lista de produtos
  - Subtotal por item
  - Total geral
  - Imagens dos produtos

- **Remover Produtos**
  - Remoção individual
  - Atualização automática do total

- **Finalizar Compra**
  - Registro de vendas no banco
  - Limpeza do carrinho
  - Redirecionamento para histórico

---

### 7. **Relatórios PDF** 📄

#### **Relatório de Compras**
- Design profissional (azul)
- Cabeçalho com logo e título
- Tabela detalhada:
  - Data, Produto, Categoria
  - Quantidade, Valor Unitário, Total
- Totais e resumos
- Rodapé com data de geração
- Visualização no navegador

#### **Relatório de Vendas**
- Design profissional (verde)
- Cabeçalho personalizado
- Tabela completa:
  - Data, Produto, Cliente
  - Quantidade, Valor, Status
- Faturamento total
- Ticket médio
- Download direto

---

### 8. **Gráficos Analíticos** 📊

#### **Histórico de Compras (Cliente)**

**Cards de Métricas:**
- Total de Compras
- Total Gasto
- Ticket Médio

**Gráficos:**
- **Gastos por Período (Barras):**
  - Últimos 7 dias
  - Valores diários
  - Tooltips com valores
  
- **Gastos por Categoria (Pizza):**
  - Distribuição por categoria
  - Percentuais
  - Cores diferenciadas

#### **Minhas Vendas (Lojista/Prestador)**

**Cards de Métricas:**
- Total de Vendas
- Faturamento Total
- Ticket Médio

**Gráficos:**
- **Vendas por Período (Linha):**
  - Últimos 7 dias
  - Tendência de faturamento
  - Área preenchida
  
- **Produtos Mais Vendidos (Rosca):**
  - Top 5 produtos
  - Quantidade vendida
  - Cores vibrantes

**Características dos Gráficos:**
- Biblioteca Chart.js
- Interativos (hover para detalhes)
- Responsivos
- Altura fixa (300px)
- Legendas compactas
- Formatação de valores (R$)

---

## 🗂️ Estrutura do Projeto

```
chrono-planck/
├── app/
│   ├── __init__.py              # Inicialização do Flask
│   ├── models.py                # Modelos do banco de dados
│   ├── routes/
│   │   ├── auth.py              # Autenticação (login, registro)
│   │   ├── main.py              # Rotas principais (dashboard, busca)
│   │   ├── stores.py            # Gerenciamento de lojas
│   │   ├── products.py          # Gerenciamento de produtos
│   │   ├── cart.py              # Carrinho de compras
│   │   └── api.py               # APIs auxiliares
│   ├── templates/
│   │   ├── base.html            # Template base
│   │   ├── login.html           # Página de login
│   │   ├── register.html        # Página de registro
│   │   ├── dashboard.html       # Dashboard principal
│   │   ├── profile.html         # Perfil do usuário
│   │   ├── search.html          # Busca de produtos
│   │   ├── product_detail.html  # Detalhes do produto (com mapa)
│   │   ├── nova_loja.html       # Cadastro de loja (com mapa)
│   │   ├── editar_loja.html     # Edição de loja (com mapa)
│   │   ├── novo_produto.html    # Cadastro de produto
│   │   ├── editar_produto.html  # Edição de produto
│   │   ├── novo_servico.html    # Cadastro de serviço
│   │   ├── editar_servico.html  # Edição de serviço
│   │   ├── minhas_vendas.html   # Vendas (com gráficos)
│   │   ├── historico_compras.html # Compras (com gráficos)
│   │   └── cart.html            # Carrinho de compras
│   └── static/
│       ├── css/
│       │   └── style.css        # Estilos customizados
│       ├── js/
│       │   └── main.js          # JavaScript principal
│       └── uploads/             # Imagens de produtos
├── instance/
│   └── mechfinder.db            # Banco de dados SQLite
├── run.py                       # Arquivo principal de execução
├── config.py                    # Configurações
├── setup_db.py                  # Script de criação do banco
├── migrate_db.py                # Script de migração
├── requirements.txt             # Dependências Python
└── README.md                    # Este arquivo
```

---

## 🗄️ Modelos do Banco de Dados

### **User**
```python
- id (Integer, PK)
- username (String, Unique)
- email (String, Unique)
- password_hash (String)
- user_type (String) # 'cliente', 'lojista', 'prestador'
- phone (String)
- created_at (DateTime)
```

### **Store**
```python
- id (Integer, PK)
- name (String)
- owner_id (Integer, FK -> User)
- category (String)
- address (String)
- number (String)        # NOVO
- cep (String)           # NOVO
- phone (String)
- email (String)
- whatsapp (String)
- latitude (Float)
- longitude (Float)
- rating (Float)
- is_active (Boolean)
```

### **Product**
```python
- id (Integer, PK)
- name (String)
- type (String) # 'product' ou 'service'
- category (String)
- description (Text)
- brand (String)
- specifications (Text)
- compatibility (Text)
- year (String)
- warranty (String)
- price (Float)
- store_id (Integer, FK -> Store)
- owner_id (Integer, FK -> User)
- image_file (String)
- is_active (Boolean)
- in_stock (Boolean)
- rating (Float)
- service_type (String)
- diferenciais (Text)
- created_at (DateTime)
```

### **Sale**
```python
- id (Integer, PK)
- product_id (Integer, FK -> Product)
- customer_id (Integer, FK -> User)
- quantity (Integer)
- total_price (Float)
- status (String)
- rating (Integer)
- review (Text)
- created_at (DateTime)
```

---

## 🛠️ Tecnologias Utilizadas

### **Backend**
- **Flask** - Framework web
- **SQLAlchemy** - ORM para banco de dados
- **Flask-Login** - Gerenciamento de sessões
- **Werkzeug** - Segurança (hash de senhas)
- **ReportLab** - Geração de PDFs

### **Frontend**
- **Bootstrap 5** - Framework CSS
- **FontAwesome** - Ícones
- **Chart.js** - Gráficos interativos
- **Leaflet** - Mapas interativos
- **JavaScript Vanilla** - Interatividade

### **APIs Externas**
- **ViaCEP** - Busca de endereços por CEP
- **Nominatim (OpenStreetMap)** - Geocodificação
- **OpenStreetMap** - Tiles de mapas
- **Google Maps** - Links de direção

### **Banco de Dados**
- **SQLite** - Desenvolvimento
- **PostgreSQL** - Produção (recomendado)

---

## 🚀 Como Executar

### **1. Pré-requisitos**
```bash
Python 3.8+
pip (gerenciador de pacotes)
```

### **2. Instalação**
```powershell
# Clone ou baixe o projeto
cd chrono-planck

# Instale as dependências
pip install -r requirements.txt
```

### **3. Configuração do Banco de Dados**
```powershell
# Criar banco de dados
python setup_db.py

# Aplicar migrações (se necessário)
python migrate_db.py
```

### **4. Executar a Aplicação**
```powershell
python run.py
```

### **5. Acessar**
```
http://localhost:5000
```

---

## 👥 Tipos de Usuário

### **Cliente**
- Buscar produtos/serviços
- Ver detalhes e localização
- Adicionar ao carrinho
- Finalizar compras
- Ver histórico de compras
- Gráficos de gastos
- Gerar relatório PDF de compras
- Contatar vendedores (WhatsApp, Tel, Email)

### **Lojista/Prestador**
- Gerenciar lojas (criar, editar, ativar/desativar)
- Cadastrar produtos/serviços
- Upload de imagens
- Ver vendas realizadas
- Gráficos de faturamento
- Gerar relatório PDF de vendas
- Receber contatos de clientes

---

## 📊 Fluxo de Uso

### **Cliente:**
1. Registra-se como cliente
2. Faz login
3. Busca produtos/serviços
4. Visualiza detalhes e localização da loja
5. Contata vendedor ou adiciona ao carrinho
6. Finaliza compra
7. Visualiza histórico e gráficos

### **Lojista:**
1. Registra-se como lojista
2. Faz login
3. Cadastra loja (com mapa e CEP)
4. Cadastra produtos/serviços
5. Recebe pedidos
6. Visualiza vendas e gráficos
7. Gera relatórios

---

## 🎨 Design e UX

- **Responsivo:** Funciona em desktop, tablet e mobile
- **Moderno:** Interface limpa e profissional
- **Intuitivo:** Navegação fácil e clara
- **Visual:** Gráficos coloridos e informativos
- **Interativo:** Mapas, tooltips, animações
- **Acessível:** Ícones e textos descritivos

---

## 🔒 Segurança

- Senhas com hash (Werkzeug)
- Sessões seguras (Flask-Login)
- Validação de propriedade (edições)
- Proteção CSRF (Flask)
- Sanitização de inputs
- Verificação de tipos de usuário

---

## 📝 Próximas Melhorias Sugeridas

- [ ] Sistema de avaliações e comentários
- [ ] Chat em tempo real
- [ ] Notificações push
- [ ] Integração com pagamentos
- [ ] Sistema de cupons/descontos
- [ ] Busca por proximidade (raio)
- [ ] Filtros avançados
- [ ] Favoritos/Wishlist
- [ ] Comparação de produtos
- [ ] API REST completa

---

## 📄 Licença

Este projeto foi desenvolvido para fins educacionais e demonstrativos.

---

## 👨‍💻 Desenvolvido com

- Flask
- Python
- JavaScript
- Bootstrap
- Chart.js
- Leaflet

---

**MechFinder - Conectando você ao mundo automotivo! 🚗✨**
