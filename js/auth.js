// Функция для обработки логина
function handleLogin(event) {
    event.preventDefault(); // Предотвращаем стандартное поведение формы

    // Перенаправляем пользователя на главную страницу (index.html)
    window.location.href = "index.html";
}

// Добавляем событие на кнопку логина
document.getElementById("login-btn").addEventListener("click", handleLogin);
