
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
