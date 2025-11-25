from flask import Blueprint, render_template, redirect, url_for, session, flash, request
from flask_login import login_required, current_user
from app.models import Product, Sale, db

cart_bp = Blueprint('cart', __name__, url_prefix='/carrinho')

@cart_bp.route('/')
@login_required
def view_cart():
    cart = session.get('cart', {})
    products = []
    total = 0
    
    for product_id, quantity in cart.items():
        product = Product.query.get(int(product_id))
        if product:
            subtotal = product.price * quantity
            total += subtotal
            products.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal
            })
    
    return render_template('cart.html', products=products, total=total)

@cart_bp.route('/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    cart = session.get('cart', {})
    quantity = int(request.form.get('quantity', 1))
    
    product_id_str = str(product_id)
    if product_id_str in cart:
        cart[product_id_str] += quantity
    else:
        cart[product_id_str] = quantity
        
    session['cart'] = cart
    flash('Produto adicionado ao carrinho!', 'success')
    return redirect(url_for('cart.view_cart'))

@cart_bp.route('/remove/<int:product_id>')
@login_required
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    product_id_str = str(product_id)
    
    if product_id_str in cart:
        del cart[product_id_str]
        session['cart'] = cart
        flash('Produto removido do carrinho.', 'info')
        
    return redirect(url_for('cart.view_cart'))

@cart_bp.route('/checkout', methods=['POST'])
@login_required
def checkout():
    cart = session.get('cart', {})
    if not cart:
        flash('Seu carrinho está vazio.', 'warning')
        return redirect(url_for('cart.view_cart'))
        
    try:
        for product_id, quantity in cart.items():
            product = Product.query.get(int(product_id))
            if product:
                sale = Sale(
                    product_id=product.id,
                    customer_id=current_user.id,
                    quantity=quantity,
                    total_price=product.price * quantity,
                    status='concluido'
                )
                db.session.add(sale)
        
        db.session.commit()
        session['cart'] = {}
        flash('Compra realizada com sucesso!', 'success')
        return redirect(url_for('main.historico_compras'))
        
    except Exception as e:
        db.session.rollback()
        flash('Erro ao processar compra. Tente novamente.', 'danger')
        return redirect(url_for('cart.view_cart'))
