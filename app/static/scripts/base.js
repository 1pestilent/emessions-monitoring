function myFunction() {
    document.getElementById("dropdown-contentlist").classList.add("show");
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