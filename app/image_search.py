# -*- coding: utf-8 -*-
"""
Módulo de Busca por Imagem usando IA com Sistema de Aprendizado
Utiliza ResNet50 pré-treinado com cache de features e histórico de buscas
"""

import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import os
import hashlib

class ImageSearchEngine:
    """
    Motor de busca por imagem usando Deep Learning com aprendizado
    """
    
    def __init__(self):
        """Inicializa o modelo ResNet50 pré-treinado"""
        print("🤖 Carregando modelo de IA para análise de imagens...")
        
        # Carregar modelo ResNet50 pré-treinado
        self.model = models.resnet50(pretrained=True)
        
        # Remover a última camada (classificação) para obter features
        self.model = torch.nn.Sequential(*list(self.model.children())[:-1])
        
        # Modo de avaliação (não treinar)
        self.model.eval()
        
        # Transformações para preprocessar imagens
        self.transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])
        
        print("✅ Modelo carregado com sucesso!")
    
    def calculate_image_hash(self, image_path):
        """
        Calcula hash MD5 da imagem para detectar mudanças
        
        Args:
            image_path: Caminho para a imagem
            
        Returns:
            Hash MD5 da imagem
        """
        try:
            with open(image_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except:
            return None
    
    def extract_features(self, image_path):
        """
        Extrai features (embeddings) de uma imagem
        
        Args:
            image_path: Caminho para a imagem
            
        Returns:
            numpy array com features da imagem
        """
        try:
            # Carregar e preprocessar imagem
            image = Image.open(image_path).convert('RGB')
            image_tensor = self.transform(image).unsqueeze(0)
            
            # Extrair features sem calcular gradientes
            with torch.no_grad():
                features = self.model(image_tensor)
            
            # Converter para numpy array e achatar
            features = features.squeeze().numpy()
            
            return features
            
        except Exception as e:
            print(f"❌ Erro ao extrair features de {image_path}: {e}")
            return None
    
    def calculate_similarity(self, features1, features2):
        """
        Calcula similaridade entre duas imagens usando cosine similarity
        
        Args:
            features1: Features da primeira imagem
            features2: Features da segunda imagem
            
        Returns:
            Score de similaridade (0 a 1, onde 1 é idêntico)
        """
        if features1 is None or features2 is None:
            return 0.0
        
        # Reshape para formato correto
        features1 = features1.reshape(1, -1)
        features2 = features2.reshape(1, -1)
        
        # Calcular cosine similarity
        similarity = cosine_similarity(features1, features2)[0][0]
        
        # Converter para escala 0-1 (cosine similarity retorna -1 a 1)
        similarity = (similarity + 1) / 2
        
        return float(similarity)
    
    def search_similar_images(self, query_image_path, product_features_dict, 
                             top_k=20, min_similarity=0.65):
        """
        Busca as imagens mais similares à imagem de consulta
        
        Args:
            query_image_path: Caminho da imagem de busca
            product_features_dict: Dicionário {product_id: features}
            top_k: Número de resultados a retornar
            min_similarity: Similaridade mínima (0.65 = 65%)
            
        Returns:
            Lista de tuplas (product_id, similarity_score) ordenada por similaridade
        """
        # Extrair features da imagem de consulta
        query_features = self.extract_features(query_image_path)
        
        if query_features is None:
            return []
        
        results = []
        
        # Comparar com cada produto
        for product_id, product_features in product_features_dict.items():
            if product_features is not None:
                # Calcular similaridade
                similarity = self.calculate_similarity(query_features, product_features)
                
                # Apenas adicionar se passar do threshold mínimo
                if similarity >= min_similarity:
                    results.append((product_id, similarity))
        
        # Ordenar por similaridade (maior primeiro)
        results.sort(key=lambda x: x[1], reverse=True)
        
        # Retornar top K resultados
        return results[:top_k]
    
    def get_or_extract_features(self, product, upload_folder, db_session):
        """
        Obtém features do cache ou extrai se necessário
        
        Args:
            product: Objeto Product
            upload_folder: Pasta de uploads
            db_session: Sessão do banco de dados
            
        Returns:
            Features do produto ou None
        """
        from app.models import ProductFeatures
        
        if not product.image_file or product.image_file == 'default_product.jpg':
            return None
        
        image_path = os.path.join(upload_folder, product.image_file)
        if not os.path.exists(image_path):
            return None
        
        # Calcular hash da imagem
        current_hash = self.calculate_image_hash(image_path)
        
        # Verificar se existe cache
        cached = ProductFeatures.query.filter_by(product_id=product.id).first()
        
        if cached and cached.image_hash == current_hash:
            # Usar cache
            return cached.features
        
        # Extrair novas features
        features = self.extract_features(image_path)
        
        if features is not None:
            # Salvar/atualizar cache
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


# Instância global do motor de busca
_search_engine = None

def get_search_engine():
    """
    Retorna a instância global do motor de busca (singleton)
    """
    global _search_engine
    if _search_engine is None:
        _search_engine = ImageSearchEngine()
    return _search_engine


def search_products_by_image(query_image_path, products, upload_folder, 
                            db_session, top_k=15, min_similarity=0.65):
    """
    Função helper para buscar produtos por imagem com cache
    
    Args:
        query_image_path: Caminho da imagem de busca
        products: Lista de objetos Product do banco de dados
        upload_folder: Pasta onde estão as imagens dos produtos
        db_session: Sessão do banco de dados
        top_k: Número de resultados (padrão: 15)
        min_similarity: Similaridade mínima (padrão: 0.65 = 65%)
        
    Returns:
        Lista de tuplas (product, similarity_score)
    """
    engine = get_search_engine()
    
    # Preparar dicionário de features (com cache)
    product_features = {}
    
    for product in products:
        features = engine.get_or_extract_features(product, upload_folder, db_session)
        if features is not None:
            product_features[product.id] = features
    
    # Buscar imagens similares
    results = engine.search_similar_images(
        query_image_path, 
        product_features, 
        top_k=top_k,
        min_similarity=min_similarity
    )
    
    # Mapear IDs para objetos Product
    product_dict = {p.id: p for p in products}
    final_results = []
    
    for product_id, similarity in results:
        if product_id in product_dict:
            final_results.append((product_dict[product_id], similarity))
    
    return final_results
