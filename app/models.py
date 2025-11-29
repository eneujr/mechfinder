from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    user_type = db.Column(db.String(20), nullable=False)  # 'lojista', 'prestador', 'cliente'
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    stores = db.relationship('Store', backref='owner', lazy='dynamic')
    products = db.relationship('Product', backref='owner', lazy='dynamic')
    purchases = db.relationship('Sale', backref='customer', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category = db.Column(db.String(50))
    address = db.Column(db.String(200))
    number = db.Column(db.String(20))
    cep = db.Column(db.String(10))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    rating = db.Column(db.Float, default=0.0)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    is_active = db.Column(db.Boolean, default=True)
    whatsapp = db.Column(db.String(20))
    
    products = db.relationship('Product', backref='store', lazy='dynamic')

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # 'product' or 'service'
    category = db.Column(db.String(50))
    description = db.Column(db.Text)
    brand = db.Column(db.String(50))
    specifications = db.Column(db.Text)
    compatibility = db.Column(db.Text)
    year = db.Column(db.String(20))
    warranty = db.Column(db.String(50))
    price = db.Column(db.Float, nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    image_file = db.Column(db.String(100), default='default_product.jpg') # For real uploads
    is_active = db.Column(db.Boolean, default=True)
    in_stock = db.Column(db.Boolean, default=True)
    rating = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Specific for services
    service_type = db.Column(db.String(50))
    diferenciais = db.Column(db.Text) # Stored as JSON string or separated by newlines

class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='concluido')
    rating = db.Column(db.Integer)
    review = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamento (customer já vem do backref em User.purchases)
    product = db.relationship('Product')

class ImageSearch(db.Model):
    """Histórico de buscas por imagem para aprendizado"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    query_image_path = db.Column(db.String(200))
    selected_product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    similarity_score = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    user = db.relationship('User', backref='image_searches')
    selected_product = db.relationship('Product', backref='image_search_selections')

class ProductFeatures(db.Model):
    """Cache de features extraídas dos produtos para performance"""
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), unique=True, nullable=False)
    features = db.Column(db.PickleType)  # Armazena o vetor de features
    image_hash = db.Column(db.String(64))  # Hash da imagem para detectar mudanças
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamento
    product = db.relationship('Product', backref=db.backref('features_cache', uselist=False))

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    type = db.Column(db.String(20), nullable=False) # 'product' ou 'service'
    description = db.Column(db.String(200))
    icon = db.Column(db.String(50), default='fas fa-tag') # Ícone FontAwesome
    is_active = db.Column(db.Boolean, default=True)
