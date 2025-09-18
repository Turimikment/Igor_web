from flask import Blueprint, jsonify, request, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Product, CartItem, Favorite, User

main_bp = Blueprint('main', __name__)

# Добавляем начальные данные о товарах
def add_sample_products():
    if Product.query.count() == 0:
        sample_products = [
            Product(name='iPhone 13', price=999.99, description='Latest iPhone', 
                   image_url='https://via.placeholder.com/200', category='Electronics'),
            Product(name='Samsung Galaxy S21', price=899.99, description='Android flagship', 
                   image_url='https://via.placeholder.com/200', category='Electronics'),
            Product(name='MacBook Pro', price=1999.99, description='Powerful laptop', 
                   image_url='https://via.placeholder.com/200', category='Computers'),
            Product(name='Nike Air Max', price=120.99, description='Comfortable shoes', 
                   image_url='https://via.placeholder.com/200', category='Clothing'),
            Product(name='Sony Headphones', price=199.99, description='Noise cancelling', 
                   image_url='https://via.placeholder.com/200', category='Electronics'),
            Product(name='Python Programming Book', price=39.99, description='Learn Python', 
                   image_url='https://via.placeholder.com/200', category='Books'),
        ]
        
        db.session.add_all(sample_products)
        db.session.commit()

@main_bp.route('/')
def index():
    add_sample_products()
    products = Product.query.all()
    return render_template('index.html', products=products)

@main_bp.route('/api/products')
def api_products():
    products = Product.query.all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'price': p.price,
        'description': p.description,
        'image_url': p.image_url,
        'category': p.category
    } for p in products])

@main_bp.route('/api/add_to_cart/<int:product_id>', methods=['POST'])
@jwt_required()
def add_to_cart(product_id):
    user_id = get_jwt_identity()
    cart_item = CartItem.query.filter_by(user_id=user_id, product_id=product_id).first()
    
    if cart_item:
        cart_item.quantity += 1
    else:
        cart_item = CartItem(user_id=user_id, product_id=product_id)
        db.session.add(cart_item)
    
    db.session.commit()
    return jsonify({'message': 'Product added to cart'})

@main_bp.route('/api/add_to_favorites/<int:product_id>', methods=['POST'])
@jwt_required()
def add_to_favorites(product_id):
    user_id = get_jwt_identity()
    favorite = Favorite.query.filter_by(user_id=user_id, product_id=product_id).first()
    
    if not favorite:
        favorite = Favorite(user_id=user_id, product_id=product_id)
        db.session.add(favorite)
        db.session.commit()
        return jsonify({'message': 'Product added to favorites'})
    
    return jsonify({'message': 'Product already in favorites'})

@main_bp.route('/cart')
@jwt_required()
def cart():
    user_id = get_jwt_identity()
    cart_items = CartItem.query.filter_by(user_id=user_id).all()
    return render_template('cart.html', cart_items=cart_items)

@main_bp.route('/favorites')
@jwt_required()
def favorites():
    user_id = get_jwt_identity()
    favorites = Favorite.query.filter_by(user_id=user_id).all()
    return render_template('favorites.html', favorites=favorites)

@main_bp.route('/api/cart')
@jwt_required()
def api_cart():
    user_id = get_jwt_identity()
    cart_items = CartItem.query.filter_by(user_id=user_id).all()
    
    return jsonify([{
        'id': item.id,
        'product': {
            'id': item.product.id,
            'name': item.product.name,
            'price': item.product.price,
            'image_url': item.product.image_url
        },
        'quantity': item.quantity
    } for item in cart_items])

@main_bp.route('/api/favorites')
@jwt_required()
def api_favorites():
    user_id = get_jwt_identity()
    favorites = Favorite.query.filter_by(user_id=user_id).all()
    
    return jsonify([{
        'id': fav.id,
        'product': {
            'id': fav.product.id,
            'name': fav.product.name,
            'price': fav.product.price,
            'image_url': fav.product.image_url
        }
    } for fav in favorites])