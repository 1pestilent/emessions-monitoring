const ctx_1 = document.getElementById('myChart1');
let chart;
let refreshInterval;

async function get_readings(sensor_id, startdate = null, enddate = null) {
  const url = new URL('api/aecs/sensors/readings/get/', window.location.origin);
  url.searchParams.append('sensor_id', sensor_id);

  if (startdate) {
    url.searchParams.append('startdate', startdate.toISOString());
  }
  if (enddate) {
    url.searchParams.append('enddate', enddate.toISOString());
  }
  
  const response = await fetch(url.toString());
  if (response.ok) {
    return await response.json();
  }
  throw new Error('Failed to fetch readings');
}

function averageData(readings, windowMinutes = 20) {
  if (!readings || readings.length === 0) return { labels: [], values: [] };

  // Сортируем данные по времени на случай, если они пришли неупорядоченными
  readings.sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));

  const averagedData = [];
  let currentWindow = [];
  let windowStartTime = null;

  for (const reading of readings) {
    const readingTime = new Date(reading.timestamp);
    
    if (!windowStartTime) {
      windowStartTime = readingTime;
    }

    // Проверяем, попадает ли текущее значение в 20-минутное окно
    const diffMinutes = (readingTime - windowStartTime) / (1000 * 60);
    
    if (diffMinutes < windowMinutes) {
      currentWindow.push(reading);
    } else {
      // Вычисляем среднее для текущего окна
      if (currentWindow.length > 0) {
        const avgValue = currentWindow.reduce((sum, r) => sum + r.value, 0) / currentWindow.length;
        const middleTime = new Date((new Date(currentWindow[0].timestamp).getTime() + 
                                   new Date(currentWindow[currentWindow.length - 1].timestamp).getTime()) / 2);
        
        averagedData.push({
          timestamp: middleTime,
          value: avgValue
        });
      }

      // Начинаем новое окно
      currentWindow = [reading];
      windowStartTime = readingTime;
    }
  }

  // Обрабатываем последнее окно
  if (currentWindow.length > 0) {
    const avgValue = currentWindow.reduce((sum, r) => sum + r.value, 0) / currentWindow.length;
    const middleTime = new Date((new Date(currentWindow[0].timestamp).getTime() + 
                               new Date(currentWindow[currentWindow.length - 1].timestamp).getTime()) / 2);
    
    averagedData.push({
      timestamp: middleTime,
      value: avgValue
    });
  }

  return {
    labels: averagedData.map(d => new Date(d.timestamp).toLocaleTimeString()),
    values: averagedData.map(d => d.value)
  };
}

async function updateCharts(sensor_id, startdate = null, enddate = null) {
  try {
    const readings = await get_readings(sensor_id, startdate, enddate);
    
    if (!readings.readings || readings.readings.length === 0) {
      console.warn('No readings data received');
      return;
    }

    // Усредняем данные за 20 минут
    const averaged = averageData(readings.readings, 20);
    
    if (chart) {
      chart.data.labels = averaged.labels;
      chart.data.datasets[0].data = averaged.values;
      chart.update();
    } else {
      chart = new Chart(ctx_1, {
        type: 'line',
        data: {
          labels: averaged.labels,
          datasets: [{
            label: `Показания датчика ${sensor_id} (усредненные за 20 минут)`,
            data: averaged.values,
            borderWidth: 2,
            borderColor: 'rgb(75, 192, 192)',
            tension: 0.1
          }]
        },
        options: {
          elements: {
            point: {
              radius: 0
            }
          },
          responsive: true,
          scales: {
            y: {
              beginAtZero: false
            },
            x: {
              title: {
                display: true,
                text: 'Время'
              }
            }
          }
        }
      });
    }
  } catch (error) {
    console.error('Failed to load readings:', error);
  }
}

document.getElementById('sensor-select').addEventListener('change', async function(e) {
  const selectedSensor = e.target.value;
  console.log(selectedSensor)
  graph.classList.remove('hidden');
  non_content.classList.add('hidden');
  
  if (selectedSensor) {
    await updateCharts(selectedSensor);

    refreshInterval = setInterval(async () => {
      await updateCharts(selectedSensor);
      console.log('График обновлён в:', new Date().toLocaleTimeString());
    }, 10000);
  }
});