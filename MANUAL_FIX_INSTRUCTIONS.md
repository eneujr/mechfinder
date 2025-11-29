# ⚠️ INSTRUÇÕES PARA CORREÇÃO MANUAL DO PRODUCT_DETAIL.HTML

## 🚨 SITUAÇÃO ATUAL

O arquivo `product_detail.html` está corrompido devido a múltiplas tentativas de edição automática.  
**Recomendação:** Aplicar as mudanças manualmente para garantir integridade.

---

## ✅ ALTERAÇÕES JÁ CONCLUÍDAS

1. ✅ **Copyright atualizado** - `base.html` linha 177
2. ✅ **Mensagem de login atualizada** - `login.html` linha 12

---

## 📝 MUDANÇAS PENDENTES NO PRODUCT_DETAIL.HTML

### Localização: Linhas 85-110 (aproximadamente)

**Encontre esta seção:**
```html
{% if store.latitude and store.longitude %}
<!-- Mapa Embutido -->
<div class="mb-3">
    <h6 class="mb-2"><i class="fas fa-map-marked-alt me-2"></i>Localização</h6>
    <div id="map" style="width: 100%; height: 200px; border-radius: 8px; border: 1px solid #ddd;"></div>
    {% endif %}  <!-- ❌ ERRO: endif no lugar errado -->
```

**Substitua por:**
```html
{% if store.latitude and store.longitude %}
<!-- Mapa Embutido -->
<div class="mb-3">
    <h6 class="mb-2"><i class="fas fa-map-marked-alt me-2"></i>Localização</h6>
    <div id="map" style="width: 100%; height: 200px; border-radius: 8px; border: 1px solid #ddd;"></div>
    <div class="mt-2 small text-muted">
        <i class="fas fa-map-pin me-1"></i>
        Lat: {{ "%.6f"|format(store.latitude) }}, Long: {{ "%.6f"|format(store.longitude) }}
    </div>
</div>

<!-- ✅ NOVO: Botão de Navegação Inteligente -->
<div class="mb-3">
    <button onclick="openNavigation({{ store.latitude }}, {{ store.longitude }}, '{{ store.name|replace(\"'\", \"\\\'\") }}')" 
            class="btn btn-primary w-100">
        <i class="fas fa-directions me-2"></i>Como Chegar
    </button>
    <div id="distance-info" class="text-muted small mt-2 text-center">
        <i class="fas fa-map-marker-distance me-1"></i>
        <span id="distance-text">Calculando distância...</span>
    </div>
</div>
{% else %}
<div class="alert alert-warning mb-3 small">
    <i class="fas fa-exclamation-triangle me-2"></i>
    Localização não disponível
</div>
{% endif %}  <!-- ✅ CORRETO: endif no final do bloco -->
```

---

## 📝 ADICIONAR FUNÇÃO JAVASCRIPT

### Localização: Antes do `</script>` final (linha ~523)

**Encontre:**
```javascript
        }
    </script>
    {% endblock %}
```

**Adicione ANTES do `</script>`:**
```javascript
        }

        // ✅ NOVO: Navegação Inteligente (Opção 4)
        function openNavigation(lat, lng, storeName) {
            const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);
            const isIOS = /iPhone|iPad|iPod/i.test(navigator.userAgent);
            
            if (isMobile) {
                if (isIOS) {
                    // iOS: Apple Maps
                    const appleMapsUrl = `maps://maps.apple.com/?daddr=${lat},${lng}`;
                    const googleMapsUrl = `https://www.google.com/maps/dir/?api=1&destination=${lat},${lng}`;
                    
                    window.location.href = appleMapsUrl;
                    setTimeout(() => window.open(googleMapsUrl, '_blank'), 1500);
                } else {
                    // Android: Google Maps app
                    const googleAppUrl = `google.navigation:q=${lat},${lng}`;
                    const googleWebUrl = `https://www.google.com/maps/dir/?api=1&destination=${lat},${lng}`;
                    
                    window.location.href = googleAppUrl;
                    setTimeout(() => window.open(googleWebUrl, '_blank'), 1500);
                }
            } else {
                // Desktop: Google Maps Web
                window.open(`https://www.google.com/maps/dir/?api=1&destination=${lat},${lng}`, '_blank');
            }
        }

        // ✅ NOVO: Calcular distância
        {% if store.latitude and store.longitude %}
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                function(position) {
                    const userLat = position.coords.latitude;
                    const userLng = position.coords.longitude;
                    const storeLat = {{ store.latitude }};
                    const storeLng = {{ store.longitude }};
                    
                    // Fórmula de Haversine
                    const R = 6371; // Raio da Terra em km
                    const dLat = (storeLat - userLat) * Math.PI / 180;
                    const dLon = (storeLng - userLng) * Math.PI / 180;
                    const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
                              Math.cos(userLat * Math.PI / 180) * Math.cos(storeLat * Math.PI / 180) *
                              Math.sin(dLon/2) * Math.sin(dLon/2);
                    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
                    const distance = R * c;
                    
                    const distanceText = document.getElementById('distance-text');
                    if (distanceText) {
                        if (distance < 1) {
                            distanceText.textContent = `A ${(distance * 1000).toFixed(0)} metros de você`;
                        } else {
                            distanceText.textContent = `A ${distance.toFixed(1)} km de você`;
                        }
                    }
                },
                function(error) {
                    const distanceInfo = document.getElementById('distance-info');
                    if (distanceInfo) {
                        distanceInfo.style.display = 'none';
                    }
                }
            );
        } else {
            const distanceInfo = document.getElementById('distance-info');
            if (distanceInfo) {
                distanceInfo.style.display = 'none';
            }
        }
        {% endif %}
    </script>
    {% endblock %}
```

---

## ✅ CHECKLIST DE VERIFICAÇÃO

Após aplicar as mudanças manualmente:

- [ ] Arquivo salvo sem erros de sintaxe
- [ ] Servidor Flask reiniciado
- [ ] Página de detalhes do produto carrega sem erros
- [ ] Mapa aparece (se loja tiver coordenadas)
- [ ] Botão "Como Chegar" aparece
- [ ] Botão "Como Chegar" funciona (abre navegação)
- [ ] Distância é calculada e exibida
- [ ] Botões de WhatsApp, telefone e email funcionam
- [ ] Botão "Comprar Agora" funciona
- [ ] Botão "Adicionar ao Carrinho" funciona

---

## 🎯 RESULTADO ESPERADO

### Desktop:
- Botão "Como Chegar" abre Google Maps Web em nova aba
- Distância exibida (ex: "A 2.5 km de você")

### iOS:
- Botão tenta abrir Apple Maps
- Fallback para Google Maps Web após 1.5s

### Android:
- Botão tenta abrir Google Maps app
- Fallback para Google Maps Web após 1.5s

---

## 📞 SUPORTE

Se encontrar problemas:
1. Verifique o console do navegador (F12)
2. Verifique logs do Flask
3. Confirme que coordenadas existem no banco de dados

---

**Arquivo criado em:** 28/11/2025  
**Status:** Pronto para aplicação manual
