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

async function get_sensors_link (location_id) {
    const response = await fetch(`/api/aecs/sensors/link/${location_id}`, {
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
        console.log(`Выбран датчик: ${selectedSensor}`);
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
    const access_token = getCookie('access_token');
    const payload = JSON.parse(atob(access_token.split('.')[1]));
    const header_username = document.getElementById('username')
    const lower_header = document.getElementById('lower-header')
    const choose_sensors = document.getElementById('sensor-select')
    header_username.textContent = payload.sub;



    var locations = await get_locations()
    locations.forEach(location => {
        const locationDiv = document.createElement('div');
        locationDiv.className = 'location-container';
        locationDiv.innerHTML = `
                <a href="#">
                    ${location.name}
                </a>`;
        locationDiv.dataset.LocationId = location.id;

        locationDiv.addEventListener('click', async () => {
            var currentLocation = locationDiv.dataset.LocationId;
            document.querySelectorAll('.location-container').forEach(container => {
                container.classList.remove('active');
            });
            
            locationDiv.classList.add('active');
            choose_sensors.innerHTML = '<option value="" disabled> Выберите нужные показания: </option>';

            sensors_by_location = await get_sensors_link(currentLocation)
            sensors_by_location.sensors.forEach(sensor => {
            const sensorOption = new Option(
                `${sensor.name} - ${sensor.serial_number}`,
                sensor.id
                );
            choose_sensors.add(sensorOption)
            });


        });
        lower_header.appendChild(locationDiv);  
    });
});


