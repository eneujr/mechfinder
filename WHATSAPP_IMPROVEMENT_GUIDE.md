# 💬 WHATSAPP MELHORADO - GUIA DE IMPLEMENTAÇÃO

## 🎯 OBJETIVO
Melhorar o botão do WhatsApp com detecção inteligente de mobile/desktop e opções adequadas.

---

## ✨ FUNCIONALIDADES

### **Mobile:**
- Detectar automaticamente
- Abrir app do WhatsApp direto
- Fallback para WhatsApp Web se app não instalado

### **Desktop:**
- Mostrar modal com opções:
  - WhatsApp Desktop (se instalado)
  - WhatsApp Web
- Usuário escolhe

---

## 📝 IMPLEMENTAÇÃO

### **1. Substituir Botão do WhatsApp**

**Localização:** `app/templates/product_detail.html` (linha ~110-115)

**Código Atual:**
```html
{% if store.whatsapp %}
<a href="https://wa.me/55{{ store.whatsapp.replace('(', '').replace(')', '').replace('-', '').replace(' ', '') }}?text=Olá!%20Tenho%20interesse%20no%20produto:%20{{ product.name|urlencode }}"
    target="_blank" class="btn btn-success">
    <i class="fab fa-whatsapp me-2"></i>Contatar via WhatsApp
</a>
{% endif %}
```

**Código Novo:**
```html
{% if store.whatsapp %}
<button type="button" class="btn btn-success w-100" 
        onclick="openWhatsApp('{{ store.whatsapp }}', '{{ product.name }}', {{ product.id }}, {{ store.id }})">
    <i class="fab fa-whatsapp me-2"></i>Contatar via WhatsApp
</button>
{% endif %}
```

---

### **2. Adicionar Modal de Opções**

**Localização:** `app/templates/product_detail.html` (antes do `{% endblock %}`)

```html
<!-- Modal WhatsApp Options -->
<div class="modal fade" id="whatsappModal" tabindex="-1">
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
            <div class="modal-header bg-success text-white">
                <h5 class="modal-title">
                    <i class="fab fa-whatsapp me-2"></i>Escolha como abrir
                </h5>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                <div class="d-grid gap-2">
                    <button type="button" class="btn btn-success btn-lg" id="whatsappDesktopBtn">
                        <i class="fas fa-desktop me-2"></i>WhatsApp Desktop
                    </button>
                    <button type="button" class="btn btn-outline-success btn-lg" id="whatsappWebBtn">
                        <i class="fas fa-globe me-2"></i>WhatsApp Web
                    </button>
                </div>
                <div class="mt-3 small text-muted">
                    <i class="fas fa-info-circle me-1"></i>
                    <strong>Desktop:</strong> Abre o aplicativo instalado no computador<br>
                    <strong>Web:</strong> Abre no navegador
                </div>
            </div>
        </div>
    </div>
</div>
```

---

### **3. Adicionar JavaScript**

**Localização:** `app/templates/product_detail.html` (dentro do `{% block scripts %}`)

```javascript
// Função para abrir WhatsApp
function openWhatsApp(phone, productName, productId, storeId) {
    // Limpar telefone
    const cleanPhone = phone.replace(/\D/g, '');
    const fullPhone = '55' + cleanPhone;
    
    // Mensagem
    const message = encodeURIComponent(`Olá! Tenho interesse no produto: ${productName}`);
    
    // Salvar contexto para retorno
    sessionStorage.setItem('whatsapp_context', JSON.stringify({
        product_id: productId,
        store_id: storeId,
        product_name: productName,
        opened_at: new Date().toISOString()
    }));
    
    // Detectar se é mobile
    const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);
    
    if (isMobile) {
        // Mobile: Tentar abrir app, fallback para web
        const appUrl = `whatsapp://send?phone=${fullPhone}&text=${message}`;
        const webUrl = `https://wa.me/${fullPhone}?text=${message}`;
        
        // Tentar abrir app
        window.location.href = appUrl;
        
        // Fallback para web após 2 segundos
        setTimeout(function() {
            window.open(webUrl, '_blank');
        }, 2000);
        
    } else {
        // Desktop: Mostrar modal com opções
        showWhatsAppModal(fullPhone, message);
    }
}

// Mostrar modal de opções (Desktop)
function showWhatsAppModal(phone, message) {
    const modal = new bootstrap.Modal(document.getElementById('whatsappModal'));
    
    // WhatsApp Desktop
    document.getElementById('whatsappDesktopBtn').onclick = function() {
        window.location.href = `whatsapp://send?phone=${phone}&text=${message}`;
        modal.hide();
    };
    
    // WhatsApp Web
    document.getElementById('whatsappWebBtn').onclick = function() {
        window.open(`https://web.whatsapp.com/send?phone=${phone}&text=${message}`, '_blank');
        modal.hide();
    };
    
    modal.show();
}

// Detectar retorno do WhatsApp
window.addEventListener('focus', function() {
    const context = sessionStorage.getItem('whatsapp_context');
    
    if (context) {
        const data = JSON.parse(context);
        const openedAt = new Date(data.opened_at);
        const now = new Date();
        const diffMinutes = (now - openedAt) / 1000 / 60;
        
        // Se passou mais de 1 minuto, considerar que houve conversa
        if (diffMinutes > 1) {
            sessionStorage.removeItem('whatsapp_context');
            showReturnModal(data);
        }
    }
});

// Modal de retorno (será implementado na melhoria 6)
function showReturnModal(data) {
    // TODO: Implementar na próxima melhoria
    console.log('Retornou do WhatsApp:', data);
}
```

---

## 🎨 FLUXO DE FUNCIONAMENTO

### **Mobile:**
```
1. Usuário clica em "Contatar via WhatsApp"
2. Sistema detecta que é mobile
3. Tenta abrir app do WhatsApp
4. Se app não abrir em 2s, abre WhatsApp Web
5. Salva contexto para detectar retorno
```

### **Desktop:**
```
1. Usuário clica em "Contatar via WhatsApp"
2. Sistema detecta que é desktop
3. Abre modal com 2 opções:
   - WhatsApp Desktop
   - WhatsApp Web
4. Usuário escolhe
5. Abre opção escolhida
6. Salva contexto para detectar retorno
```

---

## 🧪 COMO TESTAR

### **Mobile:**
```
1. Acessar produto no celular
2. Clicar em "Contatar via WhatsApp"
3. Deve abrir app do WhatsApp
4. Se não tiver app, abre WhatsApp Web
```

### **Desktop:**
```
1. Acessar produto no computador
2. Clicar em "Contatar via WhatsApp"
3. Deve abrir modal com opções
4. Escolher "WhatsApp Desktop" ou "WhatsApp Web"
5. Deve abrir opção escolhida
```

---

## 📊 BENEFÍCIOS

1. **Melhor UX:**
   - Mobile: Abre direto
   - Desktop: Usuário escolhe

2. **Mais Flexível:**
   - Suporta app e web
   - Fallback automático

3. **Rastreável:**
   - Salva contexto
   - Detecta retorno
   - Prepara para avaliação

---

## 🔄 INTEGRAÇÃO COM MELHORIA 6

O contexto salvo (`whatsapp_context`) será usado na próxima melhoria para:
- Detectar retorno ao app
- Mostrar modal de avaliação
- Registrar compra no histórico

---

## ✅ CHECKLIST

- [ ] Substituir botão do WhatsApp
- [ ] Adicionar modal de opções
- [ ] Adicionar JavaScript de detecção
- [ ] Testar em mobile
- [ ] Testar em desktop
- [ ] Verificar fallback

---

## 📝 NOTAS

### **Detecção de Mobile:**
```javascript
const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);
```

### **Formato do Telefone:**
- Entrada: `(11) 98765-4321`
- Limpo: `11987654321`
- Com DDI: `5511987654321`

### **URLs do WhatsApp:**
- **App:** `whatsapp://send?phone=...`
- **Web:** `https://wa.me/...`
- **Web Desktop:** `https://web.whatsapp.com/send?phone=...`

---

**Status:** Documentado (implementação pendente)  
**Próximo:** Corrigir product_detail.html e implementar
