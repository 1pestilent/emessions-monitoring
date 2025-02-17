
new Chart(document.getElementById('myChart'), {
type: 'line',
data: {
    labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
    datasets: [{
    label: '# of Votes',
    data: [10, 19, 3, 5, 2, 3],
    borderWidth: 2
    }]
},
options: {
    scales: {
    y: {
        beginAtZero: true
    }
    }
}
});

window.addEventListener("load", () => {
    window.addEventListener("mouseup", (e) => {
        if (!e.target.closest(".js-select")) {
            const allSelectors = document.querySelectorAll(".js-select-dropdown");
            allSelectors.forEach(select => select.classList.remove("expanded"));
            const allChevrons = document.querySelectorAll(".js-select-chevron");
            allChevrons.forEach(chevron => chevron.classList.remove("chevron__transform"));
            return;
        } else {
            const container = e.target.closest(".js-select");
            const dropdown = container.querySelector(".js-select-dropdown");
            const chevron = container.querySelector(".js-select-chevron");
            chevron.classList.toggle("chevron__transform")
            dropdown.classList.toggle("expanded");
        }
    });

    window.addEventListener("mouseup", (e) => {
        if (!e.target.closest(".js-select-item")) return;
        const container = e.target.closest(".js-select");
        const item = e.target.closest(".js-select-item");
        const input = container.querySelector(".js-select-input");
        const value = item.dataset.value;
        input.value = value;
    })
});