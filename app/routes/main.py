from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app.models import Product, Store, Sale, User, db
from sqlalchemy import or_

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return redirect(url_for('auth.login'))

@main_bp.route('/dashboard')
@login_required
def dashboard():
    user_products = Product.query.filter_by(owner_id=current_user.id).all()
    user_stores = Store.query.filter_by(owner_id=current_user.id).all()
    
    dashboard_data = {
        'total_products': len(user_products),
        'active_products': len([p for p in user_products if p.is_active]),
        'total_stores': len(user_stores),
        'recent_activity': [] # Placeholder for now
    }
    
    if current_user.user_type in ['lojista', 'prestador']:
        # Sales of my products
        my_product_ids = [p.id for p in user_products]
        vendas = Sale.query.filter(Sale.product_id.in_(my_product_ids)).all() if my_product_ids else []
        dashboard_data['total_sales'] = len(vendas)
        dashboard_data['total_revenue'] = sum(v.total_price for v in vendas)
        recent_sales = vendas[:3]
    else:
        # My purchases
        compras = Sale.query.filter_by(customer_id=current_user.id).all()
        dashboard_data['total_sales'] = len(compras)
        dashboard_data['total_revenue'] = sum(v.total_price for v in compras)
        recent_sales = compras[:3] # Actually purchases
        
    return render_template('dashboard.html', 
                         user=current_user, 
                         dashboard_data=dashboard_data,
                         products=user_products[:5],
                         recent_sales=recent_sales)

@main_bp.route('/search')
@login_required
def search():
    query = request.args.get('q', '')
    category = request.args.get('category', 'all')
    product_type = request.args.get('type', 'all')
    
    products_query = Product.query.filter_by(is_active=True)
    
    if query:
        products_query = products_query.filter(
            or_(Product.name.ilike(f'%{query}%'), Product.description.ilike(f'%{query}%'))
        )
    
    if category != 'all':
        products_query = products_query.filter_by(category=category)
    
    if product_type != 'all':
        products_query = products_query.filter_by(type=product_type)
        
    filtered_products = products_query.order_by(Product.rating.desc()).all()
    
    return render_template('search.html', 
                         products=filtered_products, 
                         search_query=query,
                         categories=['freios', 'lubrificantes', 'mecanica', 'geometria', 'funilaria', 'eletrica'],
                         user=current_user)

@main_bp.route('/profile')
@login_required
def profile():
    user_stores = Store.query.filter_by(owner_id=current_user.id).all()
    user_products = Product.query.filter_by(owner_id=current_user.id).all()
    
    compras_cliente = []
    if current_user.user_type == 'cliente':
        compras_cliente = Sale.query.filter_by(customer_id=current_user.id).order_by(Sale.created_at.desc()).limit(5).all()
    
    return render_template('profile.html',
                         user=current_user,
                         stores=user_stores,
                         products=user_products,
                         compras_cliente=compras_cliente)

@main_bp.route('/minhas-vendas')
@login_required
def minhas_vendas():
    if current_user.user_type not in ['lojista', 'prestador']:
        return redirect(url_for('main.dashboard'))
    
    my_product_ids = [p.id for p in Product.query.filter_by(owner_id=current_user.id).all()]
    if not my_product_ids:
        vendas = []
    else:
        vendas = Sale.query.filter(Sale.product_id.in_(my_product_ids)).all()
    
    # Convert to JSON-serializable format for charts
    vendas_json = []
    for venda in vendas:
        vendas_json.append({
            'id': venda.id,
            'created_at': venda.created_at.isoformat(),
            'total_price': venda.total_price,
            'quantity': venda.quantity,
            'product': {
                'name': venda.product.name,
                'category': venda.product.category
            },
            'customer': {
                'username': venda.customer.username
            }
        })
    
    return render_template('minhas_vendas.html', 
                         user=current_user, 
                         vendas=vendas,
                         vendas_json=vendas_json,
                         total_vendas=len(vendas),
                         faturamento_total=sum(v.total_price for v in vendas))

@main_bp.route('/historico-compras')
@login_required
def historico_compras():
    compras = Sale.query.filter_by(customer_id=current_user.id).order_by(Sale.created_at.desc()).all()
    
    categorias = {}
    for compra in compras:
        cat = compra.product.category if compra.product else 'outros'
        categorias[cat] = categorias.get(cat, 0) + 1
    
    # Convert to JSON-serializable format for charts
    compras_json = []
    for compra in compras:
        compras_json.append({
            'id': compra.id,
            'created_at': compra.created_at.isoformat(),
            'total_price': compra.total_price,
            'quantity': compra.quantity,
            'product': {
                'name': compra.product.name,
                'category': compra.product.category
            }
        })
        
    return render_template('historico_compras.html', 
                         user=current_user, 
                         compras=compras,
                         compras_json=compras_json,
                         total_compras=len(compras),
                         total_gasto=sum(v.total_price for v in compras),
                         categorias=categorias)
