# -*- coding: utf-8 -*-
"""
Rotas para busca por imagem com sistema de aprendizado
"""

from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app.models import Product, ImageSearch, db
from app.image_search import search_products_by_image
import os

image_search_bp = Blueprint('image_search', __name__, url_prefix='/busca-imagem')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    """Verifica se o arquivo tem extensão permitida"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@image_search_bp.route('/', methods=['GET'])
@login_required
def index():
    """Página de busca por imagem"""
    return render_template('image_search.html', user=current_user)


@image_search_bp.route('/upload', methods=['POST'])
@login_required
def upload_and_search():
    """
    Recebe upload de imagem e busca produtos similares
    """
    # Verificar se arquivo foi enviado
    if 'image' not in request.files:
        flash('Nenhuma imagem foi enviada', 'danger')
        return redirect(url_for('image_search.index'))
    
    file = request.files['image']
    
    # Verificar se arquivo foi selecionado
    if file.filename == '':
        flash('Nenhuma imagem foi selecionada', 'danger')
        return redirect(url_for('image_search.index'))
    
    # Verificar extensão do arquivo
    if not allowed_file(file.filename):
        flash('Formato de imagem não suportado. Use PNG, JPG, JPEG, GIF ou WEBP', 'danger')
        return redirect(url_for('image_search.index'))
    
    try:
        # Salvar imagem temporária
        filename = secure_filename(file.filename)
        temp_filename = f"search_{current_user.id}_{filename}"
        temp_path = os.path.join(current_app.config['UPLOAD_FOLDER'], temp_filename)
        file.save(temp_path)
        
        # Buscar todos os produtos ativos
        products = Product.query.filter_by(is_active=True).all()
        
        # Realizar busca por imagem com threshold melhorado (65%)
        results = search_products_by_image(
            temp_path,
            products,
            current_app.config['UPLOAD_FOLDER'],
            db.session,
            top_k=15,  # Reduzido para 15 melhores resultados
            min_similarity=0.65  # Mínimo de 65% de similaridade
        )
        
        # Salvar histórico de busca
        search_record = ImageSearch(
            user_id=current_user.id,
            query_image_path=temp_filename
        )
        db.session.add(search_record)
        db.session.commit()
        
        # Remover imagem temporária
        if os.path.exists(temp_path):
            os.remove(temp_path)
        
        if not results:
            flash('Nenhum produto similar encontrado com alta precisão. Tente com outra imagem ou use a busca por texto.', 'info')
            return redirect(url_for('image_search.index'))
        
        flash(f'✨ Encontrados {len(results)} produtos com alta similaridade!', 'success')
        return render_template('image_search_results.html',
                             user=current_user,
                             results=results,
                             search_id=search_record.id)
    
    except Exception as e:
        # Limpar arquivo temporário em caso de erro
        if 'temp_path' in locals() and os.path.exists(temp_path):
            os.remove(temp_path)
        
        flash(f'Erro ao processar imagem: {str(e)}', 'danger')
        return redirect(url_for('image_search.index'))


@image_search_bp.route('/record-selection', methods=['POST'])
@login_required
def record_selection():
    """
    Registra quando usuário seleciona um produto dos resultados
    (para sistema de aprendizado)
    """
    try:
        data = request.get_json()
        search_id = data.get('search_id')
        product_id = data.get('product_id')
        similarity = data.get('similarity')
        
        if search_id and product_id:
            # Atualizar registro de busca
            search_record = ImageSearch.query.get(search_id)
            if search_record and search_record.user_id == current_user.id:
                search_record.selected_product_id = product_id
                search_record.similarity_score = similarity
                db.session.commit()
                
                return jsonify({'success': True})
        
        return jsonify({'success': False}), 400
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
