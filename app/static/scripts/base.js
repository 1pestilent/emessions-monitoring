function myFunction() {
    document.getElementById("dropdown-contentlist").classList.add("show");
}

function getCookie(name) {
    let cookie = document.cookie.split('; ').find(row => row.startsWith(name + '='));
    return cookie ? cookie.split('=')[1] : null;
}

function logout() {
    document.cookie = 'access_token=;expires=Thu, 01 Jan 1970 00:00:00 UTC;';
    document.cookie = 'refresh_token=;expires=Thu, 01 Jan 1970 00:00:00 UTC;';
    window.location.href = '/login';
}

document.addEventListener("click", function(event) {
    const dropdown = document.getElementById("dropdown");
    const dropdownContent = document.getElementById("dropdown-contentlist");

    if (!dropdown.contains(event.target)) {
        if (dropdownContent.classList.contains("show")) {
            dropdownContent.classList.remove("show");
        }
    }
});

document.addEventListener('DOMContentLoaded', async function(event) {
    const access_token = getCookie('access_token');
    const payload = JSON.parse(atob(access_token.split('.')[1]));
    
    const header_username = document.getElementById('username')
    header_username.textContent = payload.sub;
});