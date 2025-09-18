// Функция для получения cookie
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

// Фильтрация товаров по категориям
document.addEventListener('DOMContentLoaded', function() {
    const filterButtons = document.querySelectorAll('.filter-btn');
    const productCards = document.querySelectorAll('.product-card');
    
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            const category = this.getAttribute('data-category');
            
            // Обновляем активную кнопку
            filterButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            // Фильтруем товары
            productCards.forEach(card => {
                if (category === 'all' || card.getAttribute('data-category') === category) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
    
    // Добавление в корзину
    document.querySelectorAll('.btn-add-cart').forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.getAttribute('data-product-id');
            addToCart(productId);
        });
    });
    
    // Добавление в избранное
    document.querySelectorAll('.btn-add-favorite').forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.getAttribute('data-product-id');
            addToFavorites(productId);
        });
    });
});

function addToCart(productId) {
    const token = getCookie('access_token');
    
    if (!token) {
        alert('Пожалуйста, войдите в систему чтобы добавить товар в корзину');
        window.location.href = '/login';
        return;
    }
    
    fetch(`/api/add_to_cart/${productId}`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
    .then(response => response.json())
    .then(data => {
        alert('Товар добавлен в корзину!');
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Ошибка при добавлении в корзину');
    });
}

function addToFavorites(productId) {
    const token = getCookie('access_token');
    
    if (!token) {
        alert('Пожалуйста, войдите в систему чтобы добавить товар в избранное');
        window.location.href = '/login';
        return;
    }
    
    fetch(`/api/add_to_favorites/${productId}`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
    .then(response => response.json())
    .then(data => {
        alert('Товар добавлен в избранное!');
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Ошибка при добавлении в избранное');
    });
}