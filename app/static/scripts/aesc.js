const ctx_1 = document.getElementById('myChart1');
let chart;
let refreshInterval;

async function get_readings(sensor_id, startdate = null, enddate = null) {
  const url = new URL('api/aecs/sensors/readings/get/', window.location.origin);
  url.searchParams.append('sensor_id', sensor_id);

  if (startdate) {
    // Преобразуем дату в строку без временной зоны
    const startdateStr = startdate.toISOString().replace('Z', '');
    url.searchParams.append('startdate', startdateStr);
  }
  if (enddate) {
    // Преобразуем дату в строку без временной зоны
    const enddateStr = enddate.toISOString().replace('Z', '');
    url.searchParams.append('enddate', enddateStr);
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

async function updateCharts(sensor_id, startdate = null, enddate = null, datainterval = 20) {
  try {
    const readings = await get_readings(sensor_id, startdate, enddate);
    
    if (!readings.readings || readings.readings.length === 0) {
      console.warn('No readings data received');
      return;
    }

    // Усредняем данные
    let averaged;
    if (datainterval !== 0) {
      averaged = averageData(readings.readings, datainterval);
    } else {
      // Если не нужно усреднение, используем исходные данные
      averaged = {
        labels: readings.readings.map(r => new Date(r.timestamp)),
        values: readings.readings.map(r => r.value)
      };
    }

    // Форматируем метки времени
    const timeFormatOptions = {
      hour: '2-digit',
      minute: '2-digit',
      day: 'numeric',
      month: 'short'
    };
    
    const displayLabels = averaged.labels.map(date => 
      date.toLocaleString('ru-RU', timeFormatOptions)
    );

    if (chart) {
      chart.data.labels = displayLabels;
      chart.data.datasets[0].data = averaged.values;
      chart.data.datasets[0].label = `Показания датчика ${sensor_id}`;
      chart.update();
    } else {
      chart = new Chart(ctx_1, {
        type: 'line',
        data: {
          labels: displayLabels,
          datasets: [{
            label: `Показания датчика ${sensor_id}`,
            data: averaged.values,
            borderWidth: 2,
            borderColor: 'rgb(75, 192, 192)',
            tension: 0.1,
            pointRadius: 0,
            pointHoverRadius: 5
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: {
              ticks: {
                maxRotation: 45,
                minRotation: 45,
                autoSkip: true,
                maxTicksLimit: 12
              },
              grid: {
                display: false
              }
            },
            y: {
              beginAtZero: false,
              ticks: {
                callback: function(value) {
                  return value.toFixed(2);
                }
              }
            }
          },
          plugins: {
            tooltip: {
              callbacks: {
                label: function(context) {
                  return `${context.dataset.label}: ${context.parsed.y.toFixed(2)}`;
                }
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

// Добавьте эти обработчики в ваш файл aesc.js

// Обработчик для кнопки "За неделю"
document.getElementById('week-btn').addEventListener('click', async function() {
  const sensorSelect = document.getElementById('sensor-select');
  const selectedSensor = sensorSelect.value;
  
  if (selectedSensor) {
    // Очищаем предыдущий интервал обновления
    if (refreshInterval) {
      clearInterval(refreshInterval);
    }
    
    // Устанавливаем даты: текущая дата и неделю назад
    const endDate = new Date();
    const startDate = new Date();
    startDate.setDate(endDate.getDate() - 7);
    
    // Обновляем график
    await updateCharts(selectedSensor, startDate, endDate, 60);
    
    // Устанавливаем новый интервал обновления
    refreshInterval = setInterval(async () => {
      await updateCharts(selectedSensor, startDate, endDate, 60);
      console.log('График обновлён в:', new Date().toLocaleTimeString());
    }, 10000);
  }
});

// Обработчик для кнопки "За месяц"
document.getElementById('month-btn').addEventListener('click', async function() {
  const sensorSelect = document.getElementById('sensor-select');
  const selectedSensor = sensorSelect.value;
  
  if (selectedSensor) {
    // Очищаем предыдущий интервал обновления
    if (refreshInterval) {
      clearInterval(refreshInterval);
    }
    
    // Устанавливаем даты: текущая дата и месяц назад
    const endDate = new Date();
    const startDate = new Date();
    startDate.setMonth(endDate.getMonth() - 1);
    
    // Обновляем график
    await updateCharts(selectedSensor, startDate, endDate, 60);
    
    // Устанавливаем новый интервал обновления
    refreshInterval = setInterval(async () => {
      await updateCharts(selectedSensor, startDate, endDate, 60);
      console.log('График обновлён в:', new Date().toLocaleTimeString());
    }, 10000);
  }
});

document.getElementById('today-btn').addEventListener('click', async function() {
  const sensorSelect = document.getElementById('sensor-select');
  const selectedSensor = sensorSelect.value;
  
  if (selectedSensor) {
    if (refreshInterval) {
      clearInterval(refreshInterval);
    }
    
    // Устанавливаем даты: текущая дата и начало дня
    const startDate = new Date();
    console.log(startDate)
    startDate.setHours(0, 0, 0, 0);
    
    // Обновляем график
    await updateCharts(selectedSensor, startDate, null, 1);
    
    // Устанавливаем новый интервал обновления
    refreshInterval = setInterval(async () => {
      await updateCharts(selectedSensor, startDate, null, 1);
      console.log('График обновлён в:', new Date().toLocaleTimeString());
    }, 10000);
  }
});

