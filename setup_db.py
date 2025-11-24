from app import create_app, db
from app.models import User, Store, Product

app = create_app()

with app.app_context():
    db.create_all()
    
    # Check if we have users
    if not User.query.first():
        print("Creating test data...")
        
        # Create users
        admin = User(username='admin', email='admin@example.com', user_type='lojista', phone='11999999999')
        admin.set_password('123456')
        
        client = User(username='cliente', email='cliente@example.com', user_type='cliente', phone='11988888888')
        client.set_password('123456')
        
        db.session.add(admin)
        db.session.add(client)
        db.session.commit()
        
        # Create store
        store = Store(name='AutoPeças Master', owner_id=admin.id, category='peças', address='Rua Exemplo, 123', phone='1133334444')
        db.session.add(store)
        db.session.commit()
        
        # Create product
        product = Product(
            name='Pastilha de Freio', 
            type='product', 
            category='freios', 
            description='Pastilha de alta performance', 
            price=150.00, 
            store_id=store.id, 
            owner_id=admin.id
        )
        db.session.add(product)
        db.session.commit()
        
        print("Test data created successfully!")
        print("Login: admin / 123456")
        print("Login: cliente / 123456")
    else:
        print("Database already contains data.")
