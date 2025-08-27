from flask import Blueprint, jsonify, request
from models import Favorite, Product, db
from auth import token_required

favorites_bp = Blueprint('favorites', __name__)

@favorites_bp.route('/api/favorites', methods=['GET'])
@token_required
def get_favorites(current_user):
    favs = Favorite.query.filter_by(user_id=current_user.id).all()
    return jsonify([
        {
            'id': f.product.id,
            'name': f.product.name,
            'price': str(f.product.price),
            'description': f.product.description,
            'image_url': f.product.image_url
        } for f in favs
    ])

@favorites_bp.route('/api/favorites/<int:product_id>', methods=['POST'])
@token_required
def add_favorite(current_user, product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'message': 'Товар не найден'}), 404
    if Favorite.query.filter_by(user_id=current_user.id, product_id=product_id).first():
        return jsonify({'message': 'Уже в избранном'}), 400
    fav = Favorite(user_id=current_user.id, product_id=product_id)
    db.session.add(fav)
    db.session.commit()
    return jsonify({'message': 'Добавлено в избранное'})

@favorites_bp.route('/api/favorites/<int:product_id>', methods=['DELETE'])
@token_required
def remove_favorite(current_user, product_id):
    fav = Favorite.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if not fav:
        return jsonify({'message': 'Не в избранном'}), 404
    db.session.delete(fav)
    db.session.commit()
    return jsonify({'message': 'Удалено из избранного'})