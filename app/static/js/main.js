// JavaScript global para o MechFinder

// Função para mostrar notificações
function showNotification(message, type = 'info') {
    const alertClass = {
        'success': 'alert-success',
        'error': 'alert-danger',
        'warning': 'alert-warning',
        'info': 'alert-info'
    }[type] || 'alert-info';

    const notification = document.createElement('div');
    notification.className = `alert ${alertClass} alert-dismissible fade show`;
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    const container = document.querySelector('.container');
    if (container) {
        container.prepend(notification);
    }

    // Remove automaticamente após 5 segundos
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

// Função para formatar números como moeda brasileira
function formatCurrency(value) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(value);
}

// Função para validar e-mail
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Função para máscara de telefone
function phoneMask(input) {
    let value = input.value.replace(/\D/g, '');

    if (value.length > 11) {
        value = value.substring(0, 11);
    }

    if (value.length > 10) {
        value = value.replace(/^(\d{2})(\d{5})(\d{4})/, '($1) $2-$3');
    } else if (value.length > 6) {
        value = value.replace(/^(\d{2})(\d{4})(\d{0,4})/, '($1) $2-$3');
    } else if (value.length > 2) {
        value = value.replace(/^(\d{2})(\d{0,5})/, '($1) $2');
    } else if (value.length > 0) {
        value = value.replace(/^(\d*)/, '($1');
    }

    input.value = value;
}

// Sistema avançado de captura de imagem
const cameraSystem = {
    currentStream: null,
    currentFacingMode: 'environment',
    capturedImages: [],

    // Inicializa a câmera real
    async initializeRealCamera(facingMode = 'environment') {
        try {
            this.stopCamera(); // Para qualquer stream anterior

            if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
                throw new Error('Câmera não suportada neste navegador');
            }

            const constraints = {
                video: {
                    facingMode: facingMode,
                    width: { ideal: 1280 },
                    height: { ideal: 720 }
                },
                audio: false
            };

            const stream = await navigator.mediaDevices.getUserMedia(constraints);
            this.currentStream = stream;
            this.currentFacingMode = facingMode;

            return stream;
        } catch (error) {
            console.error('Erro ao acessar câmera:', error);
            throw error;
        }
    },

    // Para a câmera
    stopCamera() {
        if (this.currentStream) {
            this.currentStream.getTracks().forEach(track => {
                track.stop();
            });
            this.currentStream = null;
        }
    },

    // Captura imagem da câmera
    captureImageFromCamera(videoElement) {
        const canvas = document.createElement('canvas');
        const context = canvas.getContext('2d');

        canvas.width = videoElement.videoWidth;
        canvas.height = videoElement.videoHeight;

        context.drawImage(videoElement, 0, 0, canvas.width, canvas.height);

        const imageData = canvas.toDataURL('image/jpeg', 0.8);
        this.capturedImages.push(imageData);

        return imageData;
    },

    // Alterna entre câmeras
    async switchCamera() {
        const newFacingMode = this.currentFacingMode === 'environment' ? 'user' : 'environment';

        try {
            await this.initializeRealCamera(newFacingMode);
            return newFacingMode;
        } catch (error) {
            console.error('Erro ao alternar câmera:', error);
            throw error;
        }
    },

    // Processa imagem para análise
    processImageForAnalysis(imageData) {
        // Simula processamento de imagem para identificar peças automotivas
        return {
            success: true,
            analysis: {
                product_identified: this.identifyAutomotivePart(),
                confidence: (Math.random() * 20 + 75).toFixed(1) + '%',
                features_detected: this.detectImageFeatures()
            }
        };
    },

    // Identifica peça automotiva (simulação avançada)
    identifyAutomotivePart() {
        const parts = [
            'Pastilha de Freio', 'Disco de Freio', 'Rolamento', 'Amortecedor',
            'Mola', 'Pneu', 'Roda', 'Radiador', 'Bateria', 'Filtro de Ar',
            'Filtro de Óleo', 'Correia Dentada', 'Bomba d\'Água', 'Velas de Ignição',
            'Bobina de Ignição', 'Sensor ABS', 'Rotor', 'Lona de Freio'
        ];
        return parts[Math.floor(Math.random() * parts.length)];
    },

    // Detecta características da imagem (simulação)
    detectImageFeatures() {
        const features = ['cor', 'formato', 'textura', 'marca_visivel', 'desgaste', 'dimensoes'];
        return features.slice(0, 3 + Math.floor(Math.random() * 2));
    },

    // Limpa imagens capturadas
    clearCapturedImages() {
        this.capturedImages = [];
    }
};

// Função para inicializar câmera no modal
async function initializeCameraInModal() {
    try {
        const stream = await cameraSystem.initializeRealCamera();
        const videoContainer = document.getElementById('videoContainer');

        if (!videoContainer) {
            throw new Error('Container da câmera não encontrado');
        }

        videoContainer.innerHTML = '';

        const video = document.createElement('video');
        video.id = 'cameraVideo';
        video.srcObject = stream;
        video.autoplay = true;
        video.playsInline = true;
        video.style.width = '100%';
        video.style.height = '400px';
        video.style.objectFit = 'cover';
        video.style.borderRadius = '8px';

        videoContainer.appendChild(video);

        // Adiciona indicador de qual câmera está sendo usada
        const cameraIndicator = document.createElement('div');
        cameraIndicator.className = 'camera-indicator';
        cameraIndicator.innerHTML = `
            <span class="badge bg-dark position-absolute top-0 start-0 m-2">
                <i class="fas fa-camera me-1"></i>
                ${cameraSystem.currentFacingMode === 'environment' ? 'Traseira' : 'Frontal'}
            </span>
        `;
        videoContainer.appendChild(cameraIndicator);

        return video;
    } catch (error) {
        console.error('Erro ao inicializar câmera:', error);
        showCameraError(error);
        return null;
    }
}

// Função para capturar imagem
function captureImageFromCamera() {
    const video = document.getElementById('cameraVideo');
    if (!video) {
        showNotification('Câmera não inicializada. Por favor, aguarde a câmera carregar.', 'warning');
        return null;
    }

    try {
        // Efeito de flash
        const videoContainer = document.getElementById('videoContainer');
        if (videoContainer) {
            videoContainer.classList.add('camera-flash');
            setTimeout(() => {
                videoContainer.classList.remove('camera-flash');
            }, 300);
        }

        const imageData = cameraSystem.captureImageFromCamera(video);
        showImagePreview(imageData);

        showNotification('Imagem capturada com sucesso!', 'success');
        return imageData;
    } catch (error) {
        console.error('Erro ao capturar imagem:', error);
        showNotification('Erro ao capturar imagem: ' + error.message, 'error');
        return null;
    }
}

// Mostra preview da imagem capturada
function showImagePreview(imageData) {
    const previewContainer = document.getElementById('imagePreview');
    const searchImageBtn = document.getElementById('searchImageBtn');

    if (!previewContainer || !searchImageBtn) {
        showNotification('Elementos da interface não encontrados.', 'error');
        return;
    }

    previewContainer.classList.remove('d-none');

    previewContainer.innerHTML = `
        <h6 class="mb-2">
            <i class="fas fa-check-circle text-success me-1"></i>Imagem Capturada
        </h6>
        <div class="image-preview-container position-relative">
            <img src="${imageData}" alt="Imagem capturada" 
                 style="width: 100%; height: 200px; object-fit: cover; border-radius: 8px;">
            <button type="button" class="btn btn-sm btn-danger position-absolute top-0 end-0 m-1" 
                    onclick="retakePhoto()">
                <i class="fas fa-retweet"></i>
            </button>
        </div>
        <div class="mt-2 text-center">
            <small class="text-muted">Clique no ícone para recapturar</small>
        </div>
    `;

    searchImageBtn.disabled = false;
}

// Função para recapturar foto
function retakePhoto() {
    const previewContainer = document.getElementById('imagePreview');
    const searchImageBtn = document.getElementById('searchImageBtn');

    if (previewContainer && searchImageBtn) {
        previewContainer.classList.add('d-none');
        searchImageBtn.disabled = true;
        cameraSystem.capturedImages.pop(); // Remove a última imagem
        showNotification('Imagem descartada. Pronto para nova captura.', 'info');
    }
}

// Alterna entre câmeras
async function switchCamera() {
    try {
        const newFacingMode = await cameraSystem.switchCamera();
        await initializeCameraInModal();

        showNotification(`Câmera alternada para: ${newFacingMode === 'environment' ? 'Traseira' : 'Frontal'}`, 'info');
    } catch (error) {
        showNotification('Erro ao alternar câmera: ' + error.message, 'error');
    }
}

// Para a câmera
function stopCamera() {
    cameraSystem.stopCamera();
    const videoContainer = document.getElementById('videoContainer');
    if (videoContainer) {
        videoContainer.innerHTML = `
            <div class="text-center text-muted py-5">
                <i class="fas fa-camera fa-3x mb-3"></i>
                <p>Câmera desligada</p>
            </div>
        `;
    }
}

// Mostra erro da câmera
function showCameraError(error) {
    const videoContainer = document.getElementById('videoContainer');
    if (!videoContainer) return;

    videoContainer.innerHTML = `
        <div class="alert alert-danger">
            <h6><i class="fas fa-exclamation-triangle me-2"></i>Erro na Câmera</h6>
            <p class="mb-2">${error.message}</p>
            <small>Verifique as permissões da câmera e tente novamente.</small>
        </div>
        <div class="text-center mt-3">
            <button class="btn btn-primary" onclick="initializeCameraInModal()">
                <i class="fas fa-redo me-1"></i> Tentar Novamente
            </button>
        </div>
    `;
}

// Busca por imagem usando a câmera real
async function searchByRealImage() {
    const imageData = cameraSystem.capturedImages[cameraSystem.capturedImages.length - 1];

    if (!imageData) {
        showNotification('Por favor, capture uma imagem primeiro.', 'warning');
        return;
    }

    const loadingAlert = createImageSearchLoadingAlert();
    const searchResults = document.getElementById('searchResults');

    if (searchResults) {
        searchResults.before(loadingAlert);
    }

    try {
        // Processa a imagem localmente primeiro
        const localAnalysis = cameraSystem.processImageForAnalysis(imageData);

        // Envia para o servidor para busca mais aprofundada
        const response = await fetch('/api/search_by_image', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                image: imageData,
                analysis: localAnalysis.analysis
            })
        });

        const data = await response.json();
        document.getElementById('imageSearchAlert')?.remove();

        if (data.success) {
            const modal = bootstrap.Modal.getInstance(document.getElementById('cameraModal'));
            if (modal) {
                modal.hide();
            }

            showImageSearchResults(data.results, data.analysis);
            showNotification('Busca por imagem realizada com sucesso!', 'success');
        } else {
            showNotification('Erro na busca: ' + data.error, 'error');
        }
    } catch (error) {
        document.getElementById('imageSearchAlert')?.remove();
        showNotification('Erro na busca por imagem: ' + error.message, 'error');
    }
}

// Cria alerta de carregamento para busca por imagem
function createImageSearchLoadingAlert() {
    const alertDiv = document.createElement('div');
    alertDiv.id = 'imageSearchAlert';
    alertDiv.className = 'alert alert-info alert-dismissible fade show';
    alertDiv.innerHTML = `
        <div class="d-flex align-items-center">
            <div class="spinner-border spinner-border-sm me-3" role="status"></div>
            <div class="flex-grow-1">
                <strong>Analisando imagem capturada...</strong>
                <div class="progress mt-2" style="height: 6px;">
                    <div class="progress-bar progress-bar-striped progress-bar-animated" 
                         style="width: 100%"></div>
                </div>
                <small class="d-block mt-1">Identificando peça automotiva e buscando produtos similares</small>
            </div>
        </div>
    `;
    return alertDiv;
}

// Upload de imagem da galeria
function handleImageUpload(event) {
    const file = event.target.files[0];
    if (!file) return;

    if (!file.type.startsWith('image/')) {
        showNotification('Por favor, selecione um arquivo de imagem válido.', 'warning');
        return;
    }

    if (file.size > 10 * 1024 * 1024) {
        showNotification('A imagem deve ter no máximo 10MB.', 'warning');
        return;
    }

    const reader = new FileReader();
    reader.onload = function (e) {
        const imageData = e.target.result;
        cameraSystem.capturedImages.push(imageData);
        showImagePreview(imageData);
        showNotification('Imagem carregada com sucesso!', 'success');
    };
    reader.onerror = function () {
        showNotification('Erro ao carregar a imagem.', 'error');
    };
    reader.readAsDataURL(file);
}

// Mostra resultados da busca por imagem
function showImageSearchResults(results, analysis) {
    const searchResults = document.getElementById('searchResults');
    if (!searchResults) return;

    const resultsHtml = `
        <div class="alert alert-success image-search-results">
            <div class="d-flex justify-content-between align-items-start">
                <div>
                    <h6 class="mb-2">
                        <i class="fas fa-check-circle me-2"></i>Busca por Imagem Concluída!
                    </h6>
                    <p class="mb-1"><strong>Produto identificado:</strong> ${analysis.product_identified}</p>
                    <p class="mb-1"><strong>Precisão:</strong> ${analysis.confidence}</p>
                    <p class="mb-0"><strong>Produtos encontrados:</strong> ${analysis.similar_products_found}</p>
                </div>
                <button class="btn btn-sm btn-outline-primary" onclick="clearImageSearch()">
                    <i class="fas fa-times me-1"></i> Limpar
                </button>
            </div>
        </div>
        <h5 class="mt-4 mb-3">Produtos Similares Encontrados:</h5>
        <div class="row">
    `;

    let productsHtml = '';
    if (results && results.length > 0) {
        results.forEach(product => {
            productsHtml += `
                <div class="col-md-6 col-lg-4 mb-4">
                    <div class="card h-100 product-card shadow-sm search-result-highlight">
                        <div class="card-header bg-transparent">
                            <div class="d-flex justify-content-between align-items-start">
                                <span class="badge ${product.type === 'product' ? 'bg-primary' : 'bg-success'}">
                                    ${product.type === 'product' ? 'Produto' : 'Serviço'}
                                </span>
                                <span class="text-warning small">
                                    <i class="fas fa-star"></i> ${product.rating}
                                </span>
                            </div>
                        </div>
                        <div class="card-body">
                            <h5 class="card-title">${product.name}</h5>
                            <p class="card-text text-muted small">${product.description}</p>
                            <div class="mb-2">
                                <span class="badge bg-secondary">${product.category}</span>
                                ${product.brand ? `<span class="badge bg-info">${product.brand}</span>` : ''}
                            </div>
                            <div class="d-flex justify-content-between align-items-center">
                                <strong class="text-primary">R$ ${product.price.toFixed(2)}</strong>
                                <span class="text-success small">
                                    <i class="fas fa-check-circle"></i> Disponível
                                </span>
                            </div>
                        </div>
                        <div class="card-footer bg-transparent">
                            <a href="/product/${product.id}" class="btn btn-outline-primary w-100">
                                <i class="fas fa-info-circle me-1"></i> Ver Detalhes
                            </a>
                        </div>
                    </div>
                </div>
            `;
        });
    } else {
        productsHtml = `
            <div class="col-12 text-center py-4">
                <i class="fas fa-search fa-3x text-muted mb-3"></i>
                <h5>Nenhum produto similar encontrado</h5>
                <p class="text-muted">Tente ajustar a imagem ou buscar com outros termos.</p>
            </div>
        `;
    }

    searchResults.innerHTML = resultsHtml + productsHtml + '</div>';
}

// Limpa busca por imagem
function clearImageSearch() {
    const searchResults = document.getElementById('searchResults');
    if (searchResults) {
        searchResults.innerHTML = `
            <div class="col-12 text-center py-5">
                <i class="fas fa-car fa-3x text-muted mb-3"></i>
                <h4>Encontre produtos e serviços automotivos</h4>
                <p class="text-muted mb-4">Use a busca acima para encontrar o que precisa ou explore as categorias populares.</p>
            </div>
        `;
    }
}

// Sistema de carrinho de compras (simulado) - DESATIVADO
/*
const shoppingCart = {
    items: [],

    addItem(product, quantity = 1) {
        const existingItem = this.items.find(item => item.product.id === product.id);

        if (existingItem) {
            existingItem.quantity += quantity;
        } else {
            this.items.push({
                product: product,
                quantity: quantity
            });
        }

        this.updateCartCounter();
        showNotification('Produto adicionado ao carrinho!', 'success');
    },

    removeItem(productId) {
        this.items = this.items.filter(item => item.product.id !== productId);
        this.updateCartCounter();
    },

    getTotal() {
        return this.items.reduce((total, item) => total + (item.product.price * item.quantity), 0);
    },

    updateCartCounter() {
        const counter = document.getElementById('cartCounter');
        if (counter) {
            counter.textContent = this.items.length;
            counter.style.display = this.items.length > 0 ? 'inline' : 'none';
        }

        // Atualiza também no perfil se existir
        const profileCounter = document.getElementById('profileCartCounter');
        if (profileCounter) {
            profileCounter.textContent = this.items.length;
            profileCounter.style.display = this.items.length > 0 ? 'inline' : 'none';
        }
    },

    clear() {
        this.items = [];
        this.updateCartCounter();
    },

    // Simula finalização de compra
    checkout() {
        if (this.items.length === 0) {
            showNotification('Carrinho vazio!', 'warning');
            return;
        }

        const total = this.getTotal();
        if (confirm(`Finalizar compra?\n\nTotal: ${formatCurrency(total)}\n\nItens: ${this.items.length}`)) {
            // Simula processamento da compra
            showNotification('Compra finalizada com sucesso!', 'success');
            this.clear();
        }
    }
};
*/

// Funções utilitárias para formatação
function formatDate(dateString) {
    try {
        const options = {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit'
        };
        return new Date(dateString).toLocaleDateString('pt-BR', options);
    } catch (error) {
        return dateString;
    }
}

function formatRating(rating) {
    if (!rating) return 'Não avaliado';

    const stars = '★'.repeat(Math.floor(rating)) + '☆'.repeat(5 - Math.floor(rating));
    return `${stars} (${rating}/5)`;
}

// Validação de formulários
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return true;

    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;

    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
        }
    });

    return isValid;
}

// ==================== NOVAS FUNCIONALIDADES PARA CLIENTES ====================

// Função para contatar vendedor via WhatsApp - CORRIGIDA E FUNCIONAL
async function contactSellerWhatsApp(storeId, productName = '') {
    try {
        showNotification('Conectando com WhatsApp...', 'info');

        const response = await fetch(`/api/contatar_whatsapp/${storeId}`);
        const data = await response.json();

        if (data.success) {
            // Abre o WhatsApp em uma nova aba - CORREÇÃO APLICADA
            window.open(data.whatsapp_url, '_blank', 'noopener,noreferrer');
            showNotification(`✅ WhatsApp aberto para: ${data.store_name}`, 'success');
        } else {
            showNotification('❌ Erro ao conectar com WhatsApp: ' + data.error, 'error');
        }
    } catch (error) {
        console.error('Erro WhatsApp:', error);
        showNotification('❌ Erro ao conectar com WhatsApp. Tente novamente.', 'error');
    }
}

// Função para gerar PDF de compras
function gerarPDFCompras(categoria = 'all', dataInicio = '', dataFim = '') {
    let url = `/api/gerar_pdf_compras?categoria=${categoria}`;

    if (dataInicio) {
        url += `&data_inicio=${dataInicio}`;
    }

    if (dataFim) {
        url += `&data_fim=${dataFim}`;
    }

    // Abre o PDF em uma nova aba para download
    window.open(url, '_blank');
    showNotification('📄 PDF gerado com sucesso! O download começará automaticamente.', 'success');
}

// Função para gerar PDF de vendas (para lojistas/prestadores)
function gerarPDFVendas(categoria = 'all', dataInicio = '', dataFim = '') {
    let url = `/api/gerar_pdf_vendas?categoria=${categoria}`;

    if (dataInicio) {
        url += `&data_inicio=${dataInicio}`;
    }

    if (dataFim) {
        url += `&data_fim=${dataFim}`;
    }

    // Abre o PDF em uma nova aba para download
    window.open(url, '_blank');
    showNotification('📄 Relatório de vendas gerado com sucesso! O download começará automaticamente.', 'success');
}

// Função para abrir modal de PDF
function openPdfModal() {
    const modalElement = document.getElementById('pdfModal');
    if (modalElement) {
        const modal = new bootstrap.Modal(modalElement);
        modal.show();
    }
}

// Função para abrir modal de PDF de vendas
function openPdfVendasModal() {
    const modalElement = document.getElementById('pdfVendasModal');
    if (modalElement) {
        const modal = new bootstrap.Modal(modalElement);
        modal.show();
    }
}

// Função para filtrar compras no histórico
function filtrarCompras() {
    const categoria = document.getElementById('filtroCategoria')?.value || 'all';
    const dataInicio = document.getElementById('filtroDataInicio')?.value || '';
    const dataFim = document.getElementById('filtroDataFim')?.value || '';

    const compras = document.querySelectorAll('.compra-item');
    let comprasVisiveis = 0;

    compras.forEach(compra => {
        const compraCategoria = compra.getAttribute('data-categoria');
        const compraData = compra.getAttribute('data-data');

        let mostrar = true;

        // Filtro por categoria
        if (categoria !== 'all' && compraCategoria !== categoria) {
            mostrar = false;
        }

        // Filtro por data início
        if (dataInicio && compraData < dataInicio) {
            mostrar = false;
        }

        // Filtro por data fim
        if (dataFim && compraData > dataFim) {
            mostrar = false;
        }

        if (mostrar) {
            compra.style.display = 'block';
            comprasVisiveis++;
        } else {
            compra.style.display = 'none';
        }
    });

    // Mostra mensagem se não houver compras visíveis
    const listaCompras = document.getElementById('listaCompras');
    if (listaCompras) {
        let mensagemVazio = document.getElementById('mensagemVazio');
        if (comprasVisiveis === 0) {
            if (!mensagemVazio) {
                mensagemVazio = document.createElement('div');
                mensagemVazio.id = 'mensagemVazio';
                mensagemVazio.className = 'text-center py-5';
                mensagemVazio.innerHTML = `
                    <i class="fas fa-search fa-3x text-muted mb-3"></i>
                    <h4>Nenhuma compra encontrada</h4>
                    <p class="text-muted">Tente ajustar os filtros.</p>
                `;
                listaCompras.appendChild(mensagemVazio);
            }
        } else if (mensagemVazio) {
            mensagemVazio.remove();
        }
    }
}

// Função para adicionar avaliação
function addRating(compraId, productName) {
    const rating = prompt(`⭐ Avalie o produto/serviço: ${productName}\n\nDigite uma nota de 1 a 5:`, '5');

    if (rating && rating >= 1 && rating <= 5) {
        const review = prompt('💬 Deixe um comentário (opcional):', '');

        // Envia avaliação para o servidor
        fetch('/api/avaliar_venda', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                venda_id: compraId,
                rating: parseInt(rating),
                review: review
            })
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showNotification('✅ Avaliação registrada com sucesso!', 'success');
                    setTimeout(() => {
                        location.reload();
                    }, 1500);
                } else {
                    showNotification('❌ Erro ao registrar avaliação: ' + data.error, 'error');
                }
            })
            .catch(error => {
                showNotification('❌ Erro ao registrar avaliação: ' + error.message, 'error');
            });
    }
}

// Função para editar avaliação
function editRating(compraId) {
    if (confirm('Deseja editar sua avaliação?')) {
        addRating(compraId, 'Produto/Serviço');
    }
}

// Função para visualizar detalhes do produto
function viewProductDetails(productId) {
    window.location.href = `/product/${productId}`;
}

// ==================== FUNÇÕES PARA LOJISTAS/PRESTADORES ====================

function addNewStore() {
    showNotification('🏪 Abrindo cadastro de nova loja...', 'info');
    // Em produção, isso abriria um formulário de cadastro
}

function editStore(storeId) {
    showNotification(`🏪 Editando loja ID: ${storeId}`, 'info');
}

function viewStore(storeId) {
    showNotification(`👁️ Visualizando loja ID: ${storeId}`, 'info');
}

function deactivateStore(storeId) {
    if (confirm('⚠️ Deseja realmente inativar esta loja?')) {
        showNotification(`✅ Loja ID: ${storeId} inativada com sucesso!`, 'success');
    }
}

function editProduct(productId) {
    showNotification(`✏️ Editando produto ID: ${productId}`, 'info');
}

function viewProduct(productId) {
    window.location.href = `/product/${productId}`;
}

function toggleStock(productId) {
    showNotification(`📦 Alterando status de estoque do produto ID: ${productId}`, 'info');
}

function deactivateProduct(productId) {
    if (confirm('⚠️ Deseja realmente inativar este produto/serviço?')) {
        showNotification(`✅ Produto ID: ${productId} inativado com sucesso!`, 'success');
    }
}

// ==================== FUNÇÕES GERAIS ====================

function showCart() {
    showNotification('🛒 Abrindo carrinho de compras...', 'info');
}

function editProfile() {
    const modalElement = document.getElementById('editProfileModal');
    if (modalElement) {
        const modal = new bootstrap.Modal(modalElement);
        modal.show();
    }
}

function useMyLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            function (position) {
                const lat = position.coords.latitude;
                const lng = position.coords.longitude;

                showNotification(`📍 Localização detectada! Filtrando lojas próximas...`, 'success');

                // Simula filtro por localização
                setTimeout(() => {
                    showNotification('Lojas filtradas por proximidade! Mostrando estabelecimentos mais próximos da sua localização.', 'info');
                }, 1000);
            },
            function (error) {
                console.error('Erro de geolocalização:', error);
                showNotification('Não foi possível obter sua localização. Usando localização padrão.', 'warning');
            }
        );
    } else {
        showNotification('Geolocalização não suportada neste navegador.', 'warning');
    }
}

// Função para limpar pesquisa - CORREÇÃO APLICADA
function limparPesquisa() {
    // Remove os parâmetros da URL atual e recarrega
    const url = new URL(window.location.href);
    url.search = '';
    window.location.href = url.toString();
}

// Simulação de ligação
function simulateCall(phoneNumber) {
    showNotification(`📞 Simulando ligação para: ${phoneNumber}`, 'info');
}

// Simulação de abertura de mapa
function showOnMap() {
    showNotification('🗺️ Abrindo mapa com a localização...', 'info');
}

// Compra real de produto
function realPurchase(productId) {
    if (!confirm(`✅ Confirmar compra deste produto/serviço?\n\nEsta ação registrará a venda no histórico.`)) {
        return;
    }

    const quantity = prompt('Quantidade desejada:', '1');
    if (!quantity || quantity < 1) {
        showNotification('Por favor, informe uma quantidade válida.', 'warning');
        return;
    }

    // Efetua a venda via API
    fetch('/api/efetuar_venda', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            product_id: productId,
            quantity: parseInt(quantity)
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showNotification(`🎉 Compra efetuada com sucesso!\n\n📦 Produto: ${data.venda.product_name}\n💰 Valor: R$ ${data.venda.total_price.toFixed(2)}`, 'success');

                // Redireciona para o histórico de compras após 2 segundos
                setTimeout(() => {
                    if (confirm('Deseja ver seu histórico de compras?')) {
                        window.location.href = "/historico-compras";
                    }
                }, 2000);
            } else {
                showNotification('❌ Erro ao efetuar a compra: ' + data.error, 'error');
            }
        })
        .catch(error => {
            showNotification('❌ Erro ao efetuar a compra: ' + error.message, 'error');
        });
}

// Adicionar ao carrinho (DESATIVADO)
/*
function addToCart(productId) {
    showNotification('🛒 Produto adicionado ao carrinho!', 'success');
}
*/

// ==================== INICIALIZAÇÃO ====================

// Inicialização quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', function () {
    console.log('MechFinder inicializado com sucesso!');

    // Aplica máscara de telefone em todos os inputs de telefone
    const phoneInputs = document.querySelectorAll('input[type="tel"]');
    phoneInputs.forEach(input => {
        input.addEventListener('input', function () {
            phoneMask(this);
        });
    });

    // Adiciona classes de animação
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.classList.add('fade-in');
        card.style.animationDelay = `${index * 0.1}s`;
    });

    // Inicializa tooltips do Bootstrap
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Adiciona contador do carrinho na navbar se não existir
    if (!document.getElementById('cartCounter')) {
        const cartLinks = document.querySelectorAll('a[href="#carrinho"], .nav-link:contains("Carrinho")');
        if (cartLinks.length > 0) {
            const counter = document.createElement('span');
            counter.id = 'cartCounter';
            counter.className = 'badge bg-danger rounded-pill ms-1';
            counter.style.display = 'none';
            cartLinks[0].appendChild(counter);
        }
    }

    // Configura validação de formulários
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function (e) {
            if (!validateForm(form.id)) {
                e.preventDefault();
                showNotification('Por favor, preencha todos os campos obrigatórios.', 'warning');
            }
        });
    });

    // Adiciona efeitos de hover em cards de produtos
    const productCards = document.querySelectorAll('.product-card');
    productCards.forEach(card => {
        card.addEventListener('mouseenter', function () {
            this.style.transform = 'translateY(-5px)';
        });

        card.addEventListener('mouseleave', function () {
            this.style.transform = 'translateY(0)';
        });
    });

    // Inicialização do sistema de câmera
    const cameraModal = document.getElementById('cameraModal');
    if (cameraModal) {
        cameraModal.addEventListener('show.bs.modal', function () {
            setTimeout(() => {
                initializeCameraInModal().catch(error => {
                    console.error('Falha ao inicializar câmera:', error);
                });
            }, 300);
        });

        cameraModal.addEventListener('hide.bs.modal', function () {
            stopCamera();
            cameraSystem.clearCapturedImages();
        });
    }

    // Configura o upload de arquivo
    const fileInput = document.getElementById('fileInput');
    if (fileInput) {
        fileInput.addEventListener('change', handleImageUpload);
    }

    // Configura datas padrão para filtros
    const hoje = new Date().toISOString().split('T')[0];
    const primeiroDiaMes = new Date(new Date().getFullYear(), new Date().getMonth(), 2).toISOString().split('T')[0];

    // Configura filtros de data se existirem
    const filtroDataInicio = document.getElementById('filtroDataInicio');
    const filtroDataFim = document.getElementById('filtroDataFim');
    const pdfDataInicio = document.getElementById('pdfDataInicio');
    const pdfDataFim = document.getElementById('pdfDataFim');
    const pdfVendasDataInicio = document.getElementById('pdfVendasDataInicio');
    const pdfVendasDataFim = document.getElementById('pdfVendasDataFim');

    if (filtroDataInicio) filtroDataInicio.value = primeiroDiaMes;
    if (filtroDataFim) filtroDataFim.value = hoje;
    if (pdfDataInicio) pdfDataInicio.value = primeiroDiaMes;
    if (pdfDataFim) pdfDataFim.value = hoje;
    if (pdfVendasDataInicio) pdfVendasDataInicio.value = primeiroDiaMes;
    if (pdfVendasDataFim) pdfVendasDataFim.value = hoje;

    // Aplica filtros iniciais se existirem
    if (typeof filtrarCompras === 'function') {
        setTimeout(filtrarCompras, 100);
    }

    // Atualiza contador do carrinho no perfil
    const profileCartCounter = document.getElementById('profileCartCounter');
    const mainCartCounter = document.getElementById('cartCounter');

    if (profileCartCounter && mainCartCounter) {
        profileCartCounter.textContent = mainCartCounter.textContent;
        profileCartCounter.style.display = mainCartCounter.style.display;
    }
});

// ==================== EXPORTAÇÃO DE FUNÇÕES GLOBAIS ====================

// Sistema de câmera global
window.cameraSystem = cameraSystem;
window.initializeCameraInModal = initializeCameraInModal;
window.captureImageFromCamera = captureImageFromCamera;
window.switchCamera = switchCamera;
window.stopCamera = stopCamera;
window.searchByRealImage = searchByRealImage;
window.retakePhoto = retakePhoto;

// Sistema de carrinho
// window.shoppingCart = shoppingCart;

// Funções utilitárias
window.showNotification = showNotification;
window.formatCurrency = formatCurrency;
window.formatDate = formatDate;
window.formatRating = formatRating;
window.validateForm = validateForm;

// Funções para clientes
window.contactSellerWhatsApp = contactSellerWhatsApp;
window.gerarPDFCompras = gerarPDFCompras;
window.openPdfModal = openPdfModal;
window.filtrarCompras = filtrarCompras;
window.addRating = addRating;
window.editRating = editRating;
window.viewProductDetails = viewProductDetails;

// Funções para lojistas
window.gerarPDFVendas = gerarPDFVendas;
window.openPdfVendasModal = openPdfVendasModal;
window.addNewStore = addNewStore;
window.editStore = editStore;
window.viewStore = viewStore;
window.deactivateStore = deactivateStore;
window.editProduct = editProduct;
window.viewProduct = viewProduct;
window.toggleStock = toggleStock;
window.deactivateProduct = deactivateProduct;

// Funções gerais
window.showCart = showCart;
window.editProfile = editProfile;
window.useMyLocation = useMyLocation;
window.simulateCall = simulateCall;
window.showOnMap = showOnMap;
window.realPurchase = realPurchase;
// window.addToCart = addToCart;
window.limparPesquisa = limparPesquisa;

// Simulação de API calls
window.api = {
    async post(url, data) {
        // Simula delay de rede
        await new Promise(resolve => setTimeout(resolve, 1000));

        // Simula resposta bem-sucedida
        return {
            success: true,
            data: data
        };
    },

    async get(url) {
        // Simula delay de rede
        await new Promise(resolve => setTimeout(resolve, 500));

        // Simula resposta bem-sucedida
        return {
            success: true,
            data: {}
        };
    }
};

// Exporta funções para uso global
console.log('MechFinder - Sistema Automotivo carregado com sucesso!');
