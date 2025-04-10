const ctx_1 = document.getElementById('myChart1');

new Chart(ctx_1, {
  type: 'bar',
  data: {
    labels: ['0', '2', '4', '6', '8', '10', '12', '14', '16', '18', '20', '22', '24' ],
    datasets: [{
      label: '# of Votes',
      data: [12, 19, 3, 5, 2, 3],
      borderWidth: 1
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