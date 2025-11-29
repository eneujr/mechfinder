# ✅ CHECKLIST DE VALIDAÇÃO - PRODUCT_DETAIL

## 🎯 Como Usar Este Checklist

1. Execute a aplicação: `python run.py`
2. Faça login no sistema
3. Navegue até a página de detalhes de um produto
4. Marque cada item conforme testa

---

## 📋 CHECKLIST DE TESTES

### 1. EXIBIÇÃO BÁSICA DO PRODUTO
- [ ] Nome do produto aparece corretamente
- [ ] Badge de tipo (Produto/Serviço) está visível
- [ ] Rating com estrelas está exibido
- [ ] Categoria do produto aparece
- [ ] Preço está formatado corretamente (R$ XX,XX)
- [ ] Imagem do produto carrega (ou placeholder se não houver)
- [ ] Descrição do produto está legível
- [ ] Especificações aparecem (se existirem)
- [ ] Compatibilidade aparece (se existir)
- [ ] Garantia aparece (se existir)

### 2. INFORMAÇÕES DA LOJA (SIDEBAR)
- [ ] Nome da loja aparece
- [ ] Endereço completo está visível
- [ ] CEP está formatado
- [ ] Rating da loja aparece
- [ ] **MAPA INTERATIVO** (se loja tiver lat/long):
  - [ ] Mapa carrega sem erros
  - [ ] Marcador aparece no local correto
  - [ ] Popup com nome da loja funciona
  - [ ] Coordenadas aparecem abaixo do mapa
- [ ] Botão "Como Chegar" funciona (abre Google Maps)

### 3. BOTÕES DE CONTATO
- [ ] **WhatsApp** (se loja tiver):
  - [ ] Botão aparece
  - [ ] **Mobile**: Abre app do WhatsApp
  - [ ] **Mobile**: Fallback para WhatsApp Web funciona
  - [ ] **Desktop**: Abre modal com opções
  - [ ] **Desktop**: Botão "WhatsApp Desktop" funciona
  - [ ] **Desktop**: Botão "WhatsApp Web" funciona
  - [ ] Mensagem pré-formatada está correta
- [ ] **Telefone** (se loja tiver):
  - [ ] Botão aparece
  - [ ] Link tel: funciona
- [ ] **Email** (se loja tiver):
  - [ ] Botão aparece
  - [ ] Link mailto: funciona
  - [ ] Assunto do email está correto

### 4. SISTEMA DE COMPRA
- [ ] Campo de quantidade aparece
- [ ] Valor padrão é 1
- [ ] É possível alterar a quantidade
- [ ] **Botão "Comprar Agora (Rápido)"**:
  - [ ] Adiciona ao carrinho
  - [ ] Redireciona para página do carrinho
  - [ ] Quantidade correta é adicionada
- [ ] **Botão "Adicionar ao Carrinho"**:
  - [ ] Adiciona ao carrinho
  - [ ] Permanece na mesma página
  - [ ] Mensagem de sucesso aparece

### 5. MODAL DE WHATSAPP (Desktop)
- [ ] Modal abre ao clicar no botão WhatsApp
- [ ] Título está correto
- [ ] Dois botões aparecem (Desktop e Web)
- [ ] Botão "WhatsApp Desktop" funciona
- [ ] Botão "WhatsApp Web" funciona
- [ ] Modal fecha após seleção
- [ ] Botão X fecha o modal

### 6. MODAL DE RETORNO
**Como testar:**
1. Clique no botão WhatsApp
2. Saia da aba/janela do navegador
3. Volte para a aba após 5+ segundos

- [ ] Modal de retorno aparece automaticamente
- [ ] Título "Como foi sua experiência?" aparece
- [ ] Nome da loja está correto no texto
- [ ] **Sistema de Avaliação**:
  - [ ] 5 botões de estrelas aparecem
  - [ ] Clicar em uma estrela seleciona a avaliação
  - [ ] Estrelas ficam amarelas quando selecionadas
  - [ ] Estrelas desfazem seleção corretamente
- [ ] **Campo de Comentário**:
  - [ ] Textarea aparece
  - [ ] Placeholder está correto
  - [ ] É possível digitar
- [ ] **Checkbox "Efetuei a compra"**:
  - [ ] Checkbox aparece
  - [ ] Ao marcar, campo de quantidade aparece
  - [ ] Ao desmarcar, campo de quantidade some
- [ ] **Campo de Quantidade** (se comprou):
  - [ ] Aparece ao marcar checkbox
  - [ ] Valor padrão é 1
  - [ ] É possível alterar
- [ ] **Botões do Modal**:
  - [ ] Botão "Agora Não" fecha o modal
  - [ ] Botão "Enviar" sem avaliação mostra alerta
  - [ ] Botão "Enviar" com avaliação mostra mensagem de sucesso
  - [ ] Modal fecha após enviar

### 7. CONSOLE DO NAVEGADOR
- [ ] Abrir DevTools (F12)
- [ ] Verificar aba Console
- [ ] **NÃO deve ter erros de:**
  - [ ] Jinja2 Template Syntax
  - [ ] JavaScript Syntax
  - [ ] Leaflet não carregado
  - [ ] Variáveis undefined
  - [ ] Fetch failed

### 8. TESTES DE EDGE CASES

#### Produto SEM Imagem
- [ ] Placeholder aparece
- [ ] Não quebra o layout

#### Loja SEM Coordenadas
- [ ] Mapa NÃO aparece
- [ ] Mensagem "Localização não disponível" aparece
- [ ] Botão "Como Chegar" NÃO aparece
- [ ] Resto da página funciona normalmente

#### Loja SEM WhatsApp
- [ ] Botão WhatsApp NÃO aparece
- [ ] Outros botões de contato funcionam

#### Loja SEM Telefone
- [ ] Botão Telefone NÃO aparece

#### Loja SEM Email
- [ ] Botão Email NÃO aparece

#### Produto Tipo SERVIÇO
- [ ] Badge mostra "Serviço" (verde)
- [ ] Campo "Diferenciais" aparece (se existir)
- [ ] Diferenciais aparecem como lista

---

## 🐛 REGISTRO DE BUGS ENCONTRADOS

### Bug #1
**Descrição:**  
**Passos para Reproduzir:**  
**Comportamento Esperado:**  
**Comportamento Atual:**  
**Severidade:** [ ] Crítico [ ] Alto [ ] Médio [ ] Baixo

### Bug #2
**Descrição:**  
**Passos para Reproduzir:**  
**Comportamento Esperado:**  
**Comportamento Atual:**  
**Severidade:** [ ] Crítico [ ] Alto [ ] Médio [ ] Baixo

---

## 📊 RESUMO DOS TESTES

**Total de Itens:** 80+  
**Itens Testados:** ___  
**Itens Aprovados:** ___  
**Itens Reprovados:** ___  
**Bugs Encontrados:** ___  

**Status Geral:** [ ] ✅ APROVADO [ ] ⚠️ APROVADO COM RESSALVAS [ ] ❌ REPROVADO

---

## 📝 OBSERVAÇÕES ADICIONAIS

[Escreva aqui quaisquer observações, sugestões ou comentários sobre os testes]

---

**Testado por:** _______________  
**Data:** ___/___/______  
**Navegador:** _______________  
**Versão:** _______________  
**Dispositivo:** _______________
