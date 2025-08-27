# routes/cart.py
from flask import Blueprint, jsonify, request
from models import CartItem, Product, db
from auth import token_required

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/api/cart', methods=['GET'])
@token_required
def get_cart(current_user):
    items = CartItem.query.filter_by(user_id=current_user.id).all()
    cart = []
    total = 0
    for item in items:
        product = item.product
        price = float(product.price * item.quantity)
        total += price
        cart.append({
            'id': item.id,
            'product_id': product.id,
            'name': product.name,
            'price': str(product.price),
            'quantity': item.quantity,
            'image_url': product.image_url,
            'total_price': price
        })
    return jsonify({
        'items': cart,
        'total': round(total, 2)
    })

@cart_bp.route('/api/cart', methods=['POST'])
@token_required
def add_to_cart(current_user):
    data = request.json
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)

    if not isinstance(quantity, int) or quantity < 1:
        return jsonify({'message': 'Количество должно быть положительным числом'}), 400

    product = Product.query.get(product_id)
    if not product:
        return jsonify({'message': 'Товар не найден'}), 404

    # Проверяем, есть ли уже в корзине
    cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(user_id=current_user.id, product_id=product_id, quantity=quantity)
        db.session.add(cart_item)

    db.session.commit()
    return jsonify({'message': 'Товар добавлен в корзину'})

@cart_bp.route('/api/cart/<int:item_id>', methods=['PUT'])
@token_required
def update_cart_item(current_user, item_id):
    data = request.json
    quantity = data.get('quantity')

    if not isinstance(quantity, int) or quantity < 1:
        return jsonify({'message': 'Количество должно быть положительным числом'}), 400

    item = CartItem.query.filter_by(id=item_id, user_id=current_user.id).first()
    if not item:
        return jsonify({'message': 'Элемент корзины не найден'}), 404

    item.quantity = quantity
    db.session.commit()
    return jsonify({'message': 'Количество обновлено'})

@cart_bp.route('/api/cart/<int:item_id>', methods=['DELETE'])
@token_required
def remove_from_cart(current_user, item_id):
    item = CartItem.query.filter_by(id=item_id, user_id=current_user.id).first()
    if not item:
        return jsonify({'message': 'Элемент корзины не найден'}), 404

    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Товар удалён из корзины'})

@cart_bp.route('/api/cart/clear', methods=['POST'])
@token_required
def clear_cart(current_user):
    CartItem.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    return jsonify({'message': 'Корзина очищена'})