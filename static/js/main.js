// Логин
document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    const res = await fetch('/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    });

    const data = await res.json();
    if (res.ok) {
        localStorage.setItem('token', data.access_token);
        alert('Вход выполнен');
        window.location.href = '/products';
    } else {
        alert(data.message);
    }
});

// Получение товаров
async function loadProducts() {
    const token = localStorage.getItem('token');
    if (!token) {
        alert('Пожалуйста, войдите');
        window.location.href = '/login';
        return;
    }

    const res = await fetch('/api/products', {
        headers: { 'Authorization': `Bearer ${token}` }
    });
    const products = await res.json();

    const container = document.getElementById('products');
    container.innerHTML = products.map(p => `
        <div class="card">
            <img src="${p.image_url}" alt="${p.name}">
            <h3>${p.name}</h3>
            <p>Цена: ${p.price} руб.</p>
            <p>${p.description}</p>
            <button onclick="addToFavorite(${p.id})">В избранное</button>
        </div>
    `).join('');
}

// Добавление в избранное
async function addToFavorite(productId) {
    const token = localStorage.getItem('token');
    if (!token) return;

    const res = await fetch(`/api/favorites/${productId}`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` }
    });

    if (res.ok) {
        alert('Добавлено в избранное');
    }
}
async function loadCart() {
    const token = localStorage.getItem('token');
    if (!token) {
        alert('Войдите, чтобы посмотреть корзину');
        window.location.href = '/login';
        return;
    }

    const res = await fetch('/api/cart', {
        headers: { 'Authorization': `Bearer ${token}` }
    });

    if (!res.ok) {
        alert('Ошибка загрузки корзины');
        return;
    }

    const data = await res.json();
    const container = document.getElementById('cart');
    
    if (data.items.length === 0) {
        container.innerHTML = '<p>Корзина пуста</p>';
        return;
    }

    container.innerHTML = `
        <h2>Товары в корзине</h2>
        <div id="cart-items">
            ${data.items.map(item => `
                <div class="card">
                    <img src="${item.image_url}" alt="${item.name}" style="width: 100px; height: 100px; object-fit: cover;">
                    <h3>${item.name}</h3>
                    <p>Цена: ${item.price} × ${item.quantity}</p>
                    <p><strong>Сумма: ${item.total_price.toFixed(2)} руб.</strong></p>
                    <input type="number" value="${item.quantity}" min="1" style="width: 60px" 
                           onchange="updateCartItem(${item.id}, this.value)">
                    <button onclick="removeFromCart(${item.id})">Удалить</button>
                </div>
            `).join('')}
        </div>
        <h3>Итого: ${data.total} руб.</h3>
        <button onclick="clearCart()" class="btn">Очистить корзину</button>
        <a href="/products" class="btn">Продолжить покупки</a>
    `;
}

async function updateCartItem(itemId, quantity) {
    const token = localStorage.getItem('token');
    await fetch(`/api/cart/${itemId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ quantity: parseInt(quantity) })
    });
    loadCart();
}

async function removeFromCart(itemId) {
    const token = localStorage.getItem('token');
    await fetch(`/api/cart/${itemId}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
    });
    loadCart();
}

async function clearCart() {
    const token = localStorage.getItem('token');
    await fetch('/api/cart/clear', {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` }
    });
    loadCart();
}

// Добавление в корзину (из товаров)
async function addToCart(productId, quantity = 1) {
    const token = localStorage.getItem('token');
    if (!token) {
        alert('Сначала войдите');
        return;
    }

    const res = await fetch('/api/cart', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ product_id: productId, quantity })
    });

    const data = await res.json();
    alert(data.message);
}
// Загрузка товаров при открытии страницы
loadProducts();