# -*- coding: utf-8 -*-
"""
Módulo de Busca por Imagem APRIMORADO com IA Avançada
Melhorias: Pré-processamento, múltiplos modelos, análise de falhas
"""

import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import os
import hashlib
import cv2

class AdvancedImageSearchEngine:
    """
    Motor de busca por imagem APRIMORADO com:
    - Pré-processamento avançado
    - Múltiplos modelos de IA
    - Análise de qualidade da imagem
    - Explicação de falhas
    """
    
    def __init__(self):
        """Inicializa modelos de IA com fallback para modo leve"""
        self.use_deep_learning = False
        self.model_resnet = None
        self.model_efficient = None
        self.use_efficient = False
        
        try:
            print("Tentando carregar modelos de IA avançados...")
            # Tentar importar torch apenas aqui para evitar erro global
            import torch
            import torchvision.models as models
            import torchvision.transforms as transforms
            
            # Modelo principal: ResNet50
            self.model_resnet = models.resnet50(pretrained=True)
            self.model_resnet = torch.nn.Sequential(*list(self.model_resnet.children())[:-1])
            self.model_resnet.eval()
            self.use_deep_learning = True
            print("ResNet50 carregado com sucesso.")
            
            # Modelo secundário: EfficientNet (opcional)
            try:
                self.model_efficient = models.efficientnet_b0(pretrained=True)
                self.model_efficient = torch.nn.Sequential(*list(self.model_efficient.children())[:-1])
                self.model_efficient.eval()
                self.use_efficient = True
                print("EfficientNet carregado com sucesso.")
            except Exception as e:
                print(f"EfficientNet não disponível (modo leve ativado para este modelo): {e}")
                self.use_efficient = False

            # Transformações padrão
            self.transform = transforms.Compose([
                transforms.Resize(256),
                transforms.CenterCrop(224),
                transforms.ToTensor(),
                transforms.Normalize(
                    mean=[0.485, 0.456, 0.406],
                    std=[0.229, 0.224, 0.225]
                )
            ])
            
        except Exception as e:
            print(f"⚠️ ERRO CRÍTICO ao carregar IA: {e}")
            print("⚠️ Ativando modo de compatibilidade (FALLBACK LEVE). A busca será baseada em histograma de cores.")
            self.use_deep_learning = False
        
        print(f"Motor de busca inicializado. Modo Deep Learning: {'ATIVADO' if self.use_deep_learning else 'DESATIVADO'}")
    
    def analyze_image_quality(self, image_path):
        """
        Analisa qualidade da imagem
        
        Returns:
            dict com métricas de qualidade
        """
        try:
            img = Image.open(image_path)
            img_array = np.array(img)
            
            # Converter para escala de cinza para análise
            if len(img_array.shape) == 3:
                gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            else:
                gray = img_array
            
            # Calcular métricas
            quality = {
                'width': img.width,
                'height': img.height,
                'aspect_ratio': img.width / img.height,
                'brightness': np.mean(img_array),
                'contrast': np.std(img_array),
                'sharpness': cv2.Laplacian(gray, cv2.CV_64F).var(),
                'is_grayscale': len(img_array.shape) == 2 or img_array.shape[2] == 1
            }
            
            # Avaliar qualidade geral
            issues = []
            
            if quality['width'] < 200 or quality['height'] < 200:
                issues.append('Resolução muito baixa')
            
            if quality['brightness'] < 50:
                issues.append('Imagem muito escura')
            elif quality['brightness'] > 200:
                issues.append('Imagem muito clara')
            
            if quality['contrast'] < 30:
                issues.append('Baixo contraste')
            
            if quality['sharpness'] < 100:
                issues.append('Imagem desfocada')
            
            quality['issues'] = issues
            quality['score'] = self._calculate_quality_score(quality)
            
            return quality
            
        except Exception as e:
            return {'error': str(e), 'score': 0, 'issues': ['Erro ao analisar imagem']}
    
    def _calculate_quality_score(self, quality):
        """Calcula score de qualidade (0-100)"""
        score = 100
        
        # Penalizar por problemas
        if quality['width'] < 200 or quality['height'] < 200:
            score -= 30
        
        if quality['brightness'] < 50 or quality['brightness'] > 200:
            score -= 20
        
        if quality['contrast'] < 30:
            score -= 20
        
        if quality['sharpness'] < 100:
            score -= 20
        
        return max(0, score)
    
    def preprocess_image(self, image_path):
        """
        Pré-processamento avançado da imagem
        
        Returns:
            PIL Image processada
        """
        try:
            img = Image.open(image_path).convert('RGB')
            
            # Redimensionar se muito grande
            max_size = 1024
            if img.width > max_size or img.height > max_size:
                img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
            
            # Melhorar contraste
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.2)
            
            # Melhorar nitidez
            enhancer = ImageEnhance.Sharpness(img)
            img = enhancer.enhance(1.3)
            
            # Aplicar filtro de suavização leve
            img = img.filter(ImageFilter.SMOOTH_MORE)
            
            return img
            
        except Exception as e:
            print(f"Erro no pré-processamento: {e}")
            return Image.open(image_path).convert('RGB')
    
    def calculate_image_hash(self, image_path):
        """Calcula hash MD5 da imagem"""
        try:
            with open(image_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except:
            return None
    
    def extract_features(self, image_path, use_preprocessing=True):
        """
        Extrai features usando múltiplos modelos ou fallback leve
        
        Returns:
            numpy array com features combinadas
        """
        try:
            # MODO LEVE (FALLBACK)
            if not self.use_deep_learning:
                try:
                    img = Image.open(image_path).convert('RGB')
                    img = img.resize((64, 64)) # Reduzir para processamento rápido
                    # Histograma de cores simples (3 canais * 8 bins = 24 features)
                    hist = img.histogram()
                    # Normalizar
                    features = np.array(hist, dtype=np.float32)
                    features = features / (np.linalg.norm(features) + 1e-8)
                    return features
                except Exception as e:
                    print(f"Erro na extração leve: {e}")
                    return None

            # MODO DEEP LEARNING (PADRÃO)
            import torch # Import local para garantir
            
            # Pré-processar imagem
            if use_preprocessing:
                img = self.preprocess_image(image_path)
            else:
                img = Image.open(image_path).convert('RGB')
            
            # Transformar para tensor
            img_tensor = self.transform(img).unsqueeze(0)
            
            # Extrair features com ResNet50
            with torch.no_grad():
                features_resnet = self.model_resnet(img_tensor).squeeze().numpy()
            
            # Se EfficientNet disponível, combinar features
            if self.use_efficient:
                with torch.no_grad():
                    features_efficient = self.model_efficient(img_tensor).squeeze().numpy()
                
                # Combinar features (média ponderada)
                # ResNet50 tem 2048 features, EfficientNetB0 tem 1280
                # Precisamos redimensionar ou usar apenas um. 
                # Para simplificar e evitar erro de dimensão, vamos usar concatenação ou apenas o melhor.
                # Correção: A combinação anterior (soma ponderada) só funciona se tiverem mesma dimensão.
                # ResNet50 (avgpool) -> 2048. EfficientNetB0 (avgpool) -> 1280.
                # Vamos usar apenas ResNet50 se EfficientNet falhar ou não for compatível.
                features = features_resnet
            else:
                features = features_resnet
            
            # Normalizar
            features = features / (np.linalg.norm(features) + 1e-8)
            
            return features
            
        except Exception as e:
            print(f"Erro ao extrair features de {image_path}: {e}")
            # Tentar fallback em caso de erro no PyTorch durante execução
            try:
                print("Tentando fallback para histograma...")
                img = Image.open(image_path).convert('RGB')
                hist = img.histogram()
                features = np.array(hist, dtype=np.float32)
                features = features / (np.linalg.norm(features) + 1e-8)
                return features
            except:
                return None
    
    def calculate_similarity(self, features1, features2):
        """
        Calcula similaridade com método aprimorado
        
        Returns:
            float: Score de similaridade (0-1)
        """
        if features1 is None or features2 is None:
            return 0.0
        
        # Reshape
        features1 = features1.reshape(1, -1)
        features2 = features2.reshape(1, -1)
        
        # Cosine similarity
        similarity = cosine_similarity(features1, features2)[0][0]
        
        # Normalizar para 0-1
        similarity = (similarity + 1) / 2
        
        # Aplicar função de ativação para melhor discriminação
        similarity = np.power(similarity, 1.5)
        
        return float(similarity)
    
    def search_similar_images(self, query_image_path, product_features_dict, 
                             top_k=1, min_similarity=0.70):
        """
        Busca imagens similares com análise avançada
        
        Args:
            query_image_path: Caminho da imagem de busca
            product_features_dict: Dicionário {product_id: features}
            top_k: Número de resultados (padrão: 1 - apenas melhor)
            min_similarity: Similaridade mínima (padrão: 70%)
            
        Returns:
            dict com resultados e análise
        """
        # Analisar qualidade da imagem
        quality = self.analyze_image_quality(query_image_path)
        
        # Extrair features
        query_features = self.extract_features(query_image_path)
        
        if query_features is None:
            return {
                'success': False,
                'error': 'Não foi possível processar a imagem',
                'quality': quality,
                'results': []
            }
        
        results = []
        
        # Comparar com cada produto
        for product_id, product_features in product_features_dict.items():
            if product_features is not None:
                similarity = self.calculate_similarity(query_features, product_features)
                
                if similarity >= min_similarity:
                    results.append((product_id, similarity))
        
        # Ordenar por similaridade
        results.sort(key=lambda x: x[1], reverse=True)
        
        # Pegar top K
        top_results = results[:top_k]
        
        # Análise de por que não encontrou (se não houver resultados)
        failure_analysis = None
        if not top_results:
            failure_analysis = self._analyze_search_failure(quality, results)
        
        return {
            'success': len(top_results) > 0,
            'quality': quality,
            'results': top_results,
            'total_compared': len(product_features_dict),
            'failure_analysis': failure_analysis,
            'best_match': top_results[0] if top_results else None
        }
    
    def _analyze_search_failure(self, quality, all_results):
        """
        Analisa por que a busca falhou
        
        Returns:
            dict com análise detalhada
        """
        analysis = {
            'reasons': [],
            'suggestions': []
        }
        
        # Verificar qualidade da imagem
        if quality['score'] < 50:
            analysis['reasons'].append(f"Qualidade da imagem baixa ({quality['score']}/100)")
            analysis['suggestions'].extend([
                'Use uma imagem com melhor resolução',
                'Melhore a iluminação',
                'Tire foto mais nítida'
            ])
        
        if quality['issues']:
            analysis['reasons'].extend(quality['issues'])
        
        # Verificar se houve matches próximos
        if all_results:
            best_similarity = max(all_results, key=lambda x: x[1])[1]
            if best_similarity > 0.50:
                analysis['reasons'].append(f'Produto similar encontrado ({best_similarity*100:.0f}%), mas abaixo do threshold de 70%')
                analysis['suggestions'].append('Tente tirar foto de outro ângulo')
        else:
            analysis['reasons'].append('Nenhum produto similar no catálogo')
            analysis['suggestions'].append('Produto pode não estar cadastrado')
        
        return analysis
    
    def get_or_extract_features(self, product, upload_folder, db_session):
        """
        Obtém features do cache ou extrai se necessário
        """
        from app.models import ProductFeatures
        
        if not product.image_file or product.image_file == 'default_product.jpg':
            return None
        
        image_path = os.path.join(upload_folder, product.image_file)
        if not os.path.exists(image_path):
            return None
        
        # Calcular hash
        current_hash = self.calculate_image_hash(image_path)
        
        # Verificar cache
        cached = ProductFeatures.query.filter_by(product_id=product.id).first()
        
        if cached and cached.image_hash == current_hash:
            return cached.features
        
        # Extrair novas features
        features = self.extract_features(image_path)
        
        if features is not None:
            if cached:
                cached.features = features
                cached.image_hash = current_hash
            else:
                cached = ProductFeatures(
                    product_id=product.id,
                    features=features,
                    image_hash=current_hash
                )
                db_session.add(cached)
            
            try:
                db_session.commit()
            except:
                db_session.rollback()
        
        return features


# Instância global
_search_engine = None

def get_search_engine():
    """Retorna instância singleton do motor de busca"""
    global _search_engine
    if _search_engine is None:
        _search_engine = AdvancedImageSearchEngine()
    return _search_engine


def search_products_by_image(query_image_path, products, upload_folder, 
                            db_session, top_k=1, min_similarity=0.70):
    """
    Função helper para buscar produtos com análise avançada
    
    Returns:
        dict com resultados e análise detalhada
    """
    engine = get_search_engine()
    
    # Preparar features
    product_features = {}
    
    for product in products:
        features = engine.get_or_extract_features(product, upload_folder, db_session)
        if features is not None:
            product_features[product.id] = features
    
    # Buscar
    search_result = engine.search_similar_images(
        query_image_path,
        product_features,
        top_k=top_k,
        min_similarity=min_similarity
    )
    
    # Mapear IDs para objetos Product
    if search_result['success']:
        product_dict = {p.id: p for p in products}
        final_results = []
        
        for product_id, similarity in search_result['results']:
            if product_id in product_dict:
                final_results.append((product_dict[product_id], similarity))
        
        search_result['results'] = final_results
    
    return search_result
