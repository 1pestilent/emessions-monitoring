const choose_sensors = document.getElementById('sensor-select')
const access_token = getCookie('access_token');
const payload = JSON.parse(atob(access_token.split('.')[1]));
const header_username = document.getElementById('username')
const lower_header = document.getElementById('lower-header')
const graph = document.getElementById('graph')
const non_content = document.getElementById('nonContent')

let update_interval = null

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

async function get_locations () {
    const response = await fetch('/api/aecs/sensors/locations/all', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
    });

    if (response.ok) {
        let locations = await response.json();
        console.log(locations);
        return locations;
}};

async function fetch_last_reading(sensor_id) {
    let response = await fetch(`/api/aecs/sensors/${sensor_id}/readings/last`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
    });
    if (response.ok) {
        let data = await response.json();
        return data
    }  
}

async function update_params() {
    const temp_value = document.getElementById('temperature');
    const wind_value = document.getElementById('windpull');
    const humidity_value = document.getElementById('humidity');
    const pressure_value = document.getElementById('pressure');

    let [temp_data, wind_data, humidity_data, pressure_data] = await Promise.all([
        fetch_last_reading(1),
        fetch_last_reading(2),
        fetch_last_reading(3),
        fetch_last_reading(4)
    ]);

    wind_value.innerHTML = `${wind_data.SensorReadingsModel.value} ${wind_data.symbol}`;
    temp_value.innerHTML = `${temp_data.SensorReadingsModel.value} ${temp_data.symbol}`;
    humidity_value.innerHTML = `${humidity_data.SensorReadingsModel.value} ${humidity_data.symbol}`;
    pressure_value.innerHTML = `${Math.round(pressure_data.SensorReadingsModel.value*133/1000)} k${pressure_data.symbol}`;
    console.log('Параметры обновлены!')
};

function startUpdating() {
    if (update_interval) {
        clearInterval(update_interval);
    }

    update_params();
    
    update_interval = setInterval(update_params, 60000);
}


async function get_sensors_link (location_id) {
    let response = await fetch(`/api/aecs/sensors/link/${location_id}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
    });

    if (response.ok) {
        let sensors_by_location = await response.json();
        console.log(sensors_by_location);
        return sensors_by_location;
}};

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
    header_username.textContent = payload.sub;
    var locations = await get_locations()
    startUpdating()
    locations.forEach(location => {
        var locationDiv = document.createElement('div');
        locationDiv.className = 'location-container';
        locationDiv.innerHTML = `
                <a href="#">
                    ${location.name}
                </a>`;
        locationDiv.dataset.LocationId = location.id;
        locationDiv.addEventListener('click', async () => {
            var currentLocation = locationDiv.dataset.LocationId;
            non_content.innerHTML = 'Выберите нужные показания с датчика!';
            non_content.classList.remove('hidden');
            graph.classList.add('hidden');
            document.querySelectorAll('.location-container').forEach(container => {
                container.classList.remove('active');
            });
            locationDiv.classList.add('active');
            choose_sensors.classList.remove('hidden')
            choose_sensors.innerHTML = '<option value="" disabled selected> Выберите нужные показания: </option>';

            sensors_by_location = await get_sensors_link(currentLocation)
            const sensors = sensors_by_location.sensors
            sensors.forEach(sensor => {
            let sensorOption = new Option(
                `${sensor.name} - ${sensor.serial_number}`,
                sensor.id
                );
            choose_sensors.add(sensorOption)
            });
        });
        lower_header.appendChild(locationDiv);
    });
});

