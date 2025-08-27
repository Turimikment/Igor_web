from flask import Blueprint, jsonify, request
from models import Product, db
from auth import token_required

products_bp = Blueprint('products', __name__)

@products_bp.route('/api/products', methods=['GET'])
@token_required
def get_products(current_user):
    products = Product.query.all()
    return jsonify([
        {
            'id': p.id,
            'name': p.name,
            'price': str(p.price),
            'description': p.description,
            'image_url': p.image_url
        } for p in products
    ])

@products_bp.route('/api/products', methods=['POST'])
@token_required
def create_product(current_user):
    data = request.json
    product = Product(
        name=data['name'],
        price=data['price'],
        description=data['description'],
        image_url=data.get('image_url')
    )
    db.session.add(product)
    db.session.commit()
    return jsonify({'message': 'Товар добавлен', 'id': product.id}), 201