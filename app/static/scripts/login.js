function validateInputs(username, password) {
    const errors = [];

    if (!username || !/^[A-Za-z0-9\.]+$/.test(username) || username.length > 32) {
        errors.push('Логин может содержать только английские буквы, цифры.');
    }

    if (!password || password.length < 6) {
        errors.push('Пароль должен содержать не менее 6 символов.');
    }

    if (/[а-яА-Я]/.test(password)) {
        errors.push('Пароль не должен содержать кириллицу.');
    }

    return errors;
}

document.getElementById('loginForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const errorMessage = document.getElementById('errorMessage');
    const submitButton = document.getElementById('submitButton');
    const loadingSpinner = document.getElementById('loadingSpinner');

    errorMessage.style.display = 'none';
    errorMessage.textContent = '';

    const errors = validateInputs(username, password);
    if (errors.length > 0) {
        errorMessage.textContent = errors.join(' ');
        errorMessage.style.display = 'block';
        return;
    }

    submitButton.disabled = true;
    loadingSpinner.style.display = 'block';

    try {
        const formData = new URLSearchParams();
        formData.append('username', username);
        formData.append('password', password);

        const response = await fetch('/auth/token', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: formData,
        });
        console.log('Status:', response.status);
        console.log('Headers:', [...response.headers]);
        if (response.ok) {
            window.location.href = '/';
        } else {
            errorMessage.textContent = 'Неверный логин или пароль! Если Вы забыли пароль - обратитесь к системному администратору!';
            errorMessage.style.display = 'block';
        }
    } catch (error) {
        errorMessage.textContent = 'Сервер не отвечает.';
        errorMessage.style.display = 'block';
    } finally {
        submitButton.disabled = false;
        loadingSpinner.style.display = 'none';
    }
});