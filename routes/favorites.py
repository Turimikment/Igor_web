from flask import Blueprint, jsonify, request
from models import Favorite, Product, db
from auth import token_required

favorites_bp = Blueprint('favorites', __name__)

@favorites_bp.route('/api/favorites', methods=['GET'])
@token_required
def get_favorites(current_user):
    favorites = current_user.favorites
    return jsonify([
        {
            'id': f.product_id,
            'name': f.product.name,
            'price': str(f.product.price),
            'description': f.product.description,
            'image_url': f.product.image_url
        } for f in favorites
    ])

@favorites_bp.route('/api/favorites/<int:product_id>', methods=['POST'])
@token_required
def add_to_favorite(current_user, product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'message': 'Product not found'}), 404
    favorite = Favorite(user_id=current_user.id, product_id=product_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify({'message': 'Added to favorites'})

@favorites_bp.route('/api/favorites/<int:product_id>', methods=['DELETE'])
@token_required
def remove_from_favorite(current_user, product_id):
    favorite = Favorite.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if not favorite:
        return jsonify({'message': 'Not in favorites'}), 404
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({'message': 'Removed from favorites'})