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

// Загрузка товаров при открытии страницы
loadProducts();