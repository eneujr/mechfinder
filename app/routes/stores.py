from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Store, db

stores_bp = Blueprint('stores', __name__)

@stores_bp.route('/editar/loja/<int:store_id>', methods=['GET', 'POST'])
@login_required
def editar_loja(store_id):
    store = Store.query.get_or_404(store_id)
    
    # Verify ownership
    if store.owner_id != current_user.id:
        flash('Você não tem permissão para editar esta loja.', 'danger')
        return redirect(url_for('main.profile'))
    
    if request.method == 'POST':
        # Update store fields
        store.name = request.form.get('nome')
        store.category = request.form.get('categoria')
        store.address = request.form.get('endereco')
        store.number = request.form.get('numero')
        store.cep = request.form.get('cep')
        store.phone = request.form.get('telefone')
        store.email = request.form.get('email')
        store.whatsapp = request.form.get('whatsapp')
        
        # Optional coordinates
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        
        if latitude:
            store.latitude = float(latitude)
        if longitude:
            store.longitude = float(longitude)
        
        db.session.commit()
        flash('Loja atualizada com sucesso!', 'success')
        return redirect(url_for('main.profile'))
    
    return render_template('editar_loja.html', user=current_user, store=store)

@stores_bp.route('/nova/loja', methods=['GET', 'POST'])
@login_required
def nova_loja():
    if current_user.user_type not in ['lojista', 'prestador']:
        flash('Apenas lojistas e prestadores podem cadastrar lojas.', 'danger')
        return redirect(url_for('main.profile'))
    
    if request.method == 'POST':
        nova_loja = Store(
            name=request.form.get('nome'),
            category=request.form.get('categoria'),
            address=request.form.get('endereco'),
            number=request.form.get('numero'),
            cep=request.form.get('cep'),
            phone=request.form.get('telefone'),
            email=request.form.get('email'),
            whatsapp=request.form.get('whatsapp'),
            owner_id=current_user.id,
            rating=5.0
        )
        
        # Optional coordinates
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        
        if latitude:
            nova_loja.latitude = float(latitude)
        if longitude:
            nova_loja.longitude = float(longitude)
        
        db.session.add(nova_loja)
        db.session.commit()
        flash('Loja cadastrada com sucesso!', 'success')
        return redirect(url_for('main.profile'))
    
    return render_template('nova_loja.html', user=current_user)

@stores_bp.route('/desativar/loja/<int:store_id>', methods=['POST'])
@login_required
def desativar_loja(store_id):
    store = Store.query.get_or_404(store_id)
    
    # Verify ownership
    if store.owner_id != current_user.id:
        flash('Você não tem permissão para desativar esta loja.', 'danger')
        return redirect(url_for('main.profile'))
    
    store.is_active = not store.is_active
    db.session.commit()
    
    status = 'ativada' if store.is_active else 'desativada'
    flash(f'Loja {status} com sucesso!', 'success')
    return redirect(url_for('main.profile'))
