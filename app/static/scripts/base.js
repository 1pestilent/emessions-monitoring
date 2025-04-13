const choose_sensors = document.getElementById('sensor-select')
const access_token = getCookie('access_token');
const payload = JSON.parse(atob(access_token.split('.')[1]));
const header_username = document.getElementById('username')
const lower_header = document.getElementById('lower-header')

const graph = document.getElementById('graph')
const non_content = document.getElementById('nonContent')

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
    let temp_data = await fetch_last_reading(1)
    let temp_value = document.getElementById('temperature')

    temp_value.innerHTML = `${temp_data.SensorReadingsModel.value} ${temp_data.symbol}`;
    update_interval = setInterval(update_params, 5000)
    console.log('Параметры обновлены!')
};

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

document.getElementById('sensor-select').addEventListener('change', function(e) {
    const selectedSensor = e.target.value;
    if (selectedSensor) {
        graph.classList.remove('hidden')
        non_content.classList.add('hidden')
    }
});

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
    await fetch_last_reading(1)
    await update_params()
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
            sensors_by_location.sensors.forEach(sensor => {
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

