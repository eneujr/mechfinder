from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, jsonify
from flask_login import login_required, current_user
from app.models import Product, Store, db
import random
import os
from werkzeug.utils import secure_filename

products_bp = Blueprint('products', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

def save_product_image(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Add random prefix to avoid collision
        filename = f"{random.randint(1000, 9999)}_{filename}"
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        return filename
    return 'default_product.jpg'

@products_bp.route('/product/<int:product_id>')
@login_required
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    store = Store.query.get(product.store_id)
    similar_stores = Store.query.order_by(Store.rating.desc()).limit(3).all()
    
    return render_template('product_detail.html',
                         product=product,
                         store=store,
                         similar_stores=similar_stores,
                         user=current_user)

@products_bp.route('/cadastro/produto', methods=['GET', 'POST'])
@login_required
def cadastro_produto():
    if current_user.user_type not in ['lojista', 'prestador']:
        return redirect(url_for('auth.login'))
    
    store = Store.query.filter_by(owner_id=current_user.id).first()
    if not store:
        store = Store(name=f"Loja de {current_user.username}", owner_id=current_user.id, category='geral')
        db.session.add(store)
        db.session.commit()

    if request.method == 'POST':
        image_file = save_product_image(request.files.get('imagem'))
        
        novo_produto = Product(
            name=request.form.get('nome'),
            type='product',
            category=request.form.get('categoria'),
            description=request.form.get('descricao'),
            brand=request.form.get('marca'),
            specifications=request.form.get('especificacoes'),
            compatibility=request.form.get('compatibilidade'),
            year=request.form.get('ano_fabricacao'),
            warranty=request.form.get('garantia'),
            price=float(request.form.get('preco', 0)),
            store_id=store.id,
            owner_id=current_user.id,
            image_file=image_file,
            rating=round(random.uniform(4.0, 5.0), 1)
        )
        
        db.session.add(novo_produto)
        db.session.commit()
        flash('Produto cadastrado com sucesso!', 'success')
        return redirect(url_for('main.profile'))
    
    user_products = Product.query.filter_by(owner_id=current_user.id, type='product').limit(3).all()
    return render_template('cadastro_produto.html', user=current_user, products=user_products)

@products_bp.route('/cadastro/servico', methods=['GET', 'POST'])
@login_required
def cadastro_servico():
    if current_user.user_type not in ['lojista', 'prestador']:
        return redirect(url_for('auth.login'))
    
    store = Store.query.filter_by(owner_id=current_user.id).first()
    if not store:
        store = Store(name=f"Oficina de {current_user.username}", owner_id=current_user.id, category='servicos')
        db.session.add(store)
        db.session.commit()

    if request.method == 'POST':
        # Services might have before/after photos, but for now let's use the main image field
        image_file = save_product_image(request.files.get('imagem'))
        
        novo_servico = Product(
            name=request.form.get('nome_servico'),
            type='service',
            category=request.form.get('categoria_servico'),
            description=request.form.get('descricao_servico'),
            specifications=request.form.get('especificacoes_servico'),
            compatibility=request.form.get('compatibilidade_servico'),
            warranty=request.form.get('garantia_servico'),
            price=float(request.form.get('preco_servico', 0)),
            store_id=store.id,
            owner_id=current_user.id,
            image_file=image_file,
            service_type=request.form.get('categoria_servico'),
            diferenciais=request.form.get('diferenciais'),
            rating=round(random.uniform(4.0, 5.0), 1)
        )
        
        db.session.add(novo_servico)
        db.session.commit()
        flash('Serviço cadastrado com sucesso!', 'success')
        return redirect(url_for('main.profile'))
    
    user_services = Product.query.filter_by(owner_id=current_user.id, type='service').limit(3).all()
    return render_template('cadastro_servico.html', user=current_user, products=user_services)

@products_bp.route('/editar/produto/<int:product_id>', methods=['GET', 'POST'])
@login_required
def editar_produto(product_id):
    product = Product.query.get_or_404(product_id)
    
    # Verify ownership
    if product.owner_id != current_user.id:
        flash('Você não tem permissão para editar este produto.', 'danger')
        return redirect(url_for('main.profile'))
    
    if request.method == 'POST':
        # Handle image update
        if request.files.get('imagem'):
            image_file = save_product_image(request.files.get('imagem'))
            if image_file != 'default_product.jpg':
                product.image_file = image_file
        
        # Update product fields
        product.name = request.form.get('nome')
        product.category = request.form.get('categoria')
        product.description = request.form.get('descricao')
        product.brand = request.form.get('marca')
        product.specifications = request.form.get('especificacoes')
        product.compatibility = request.form.get('compatibilidade')
        product.year = request.form.get('ano_fabricacao')
        product.warranty = request.form.get('garantia')
        product.price = float(request.form.get('preco', 0))
        
        db.session.commit()
        flash('Produto atualizado com sucesso!', 'success')
        return redirect(url_for('main.profile'))
    
    return render_template('editar_produto.html', user=current_user, product=product)

@products_bp.route('/editar/servico/<int:product_id>', methods=['GET', 'POST'])
@login_required
def editar_servico(product_id):
    product = Product.query.get_or_404(product_id)
    
    # Verify ownership
    if product.owner_id != current_user.id:
        flash('Você não tem permissão para editar este serviço.', 'danger')
        return redirect(url_for('main.profile'))
    
    if request.method == 'POST':
        # Handle image update
        if request.files.get('imagem'):
            image_file = save_product_image(request.files.get('imagem'))
            if image_file != 'default_product.jpg':
                product.image_file = image_file
        
        # Update service fields
        product.name = request.form.get('nome_servico')
        product.category = request.form.get('categoria_servico')
        product.description = request.form.get('descricao_servico')
        product.specifications = request.form.get('especificacoes_servico')
        product.compatibility = request.form.get('compatibilidade_servico')
        product.warranty = request.form.get('garantia_servico')
        product.price = float(request.form.get('preco_servico', 0))
        product.service_type = request.form.get('categoria_servico')
        product.diferenciais = request.form.get('diferenciais')
        
        db.session.commit()
        flash('Serviço atualizado com sucesso!', 'success')
        return redirect(url_for('main.profile'))
    
    return render_template('editar_servico.html', user=current_user, product=product)

@products_bp.route('/desativar/<int:product_id>', methods=['POST'])
@login_required
def desativar_produto(product_id):
    product = Product.query.get_or_404(product_id)
    
    # Verify ownership
    if product.owner_id != current_user.id:
        return jsonify({'error': 'Não autorizado'}), 403
    
    product.is_active = not product.is_active
    db.session.commit()
    
    status = 'ativado' if product.is_active else 'desativado'
    flash(f'Produto {status} com sucesso!', 'success')
    return redirect(url_for('main.profile'))
