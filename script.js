var map = L.map('mapid').setView([37.7749, -122.4194], 13);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
  maxZoom: 18,
}).addTo(map);

var marker = L.marker([37.7749, -122.4194]).addTo(map);

function onLocationFound(e) {
  var radius = e.accuracy / 2;

  L.marker(e.latlng).addTo(map)
    .bindPopup("You are within " + radius + " meters of this point").openPopup();
}

function onLocationError(e) {
  alert(e.message);
}

map.on('locationfound', onLocationFound);
map.on('locationerror', onLocationError);

function checkParkingSpot() {
  var currentLocation = marker.getLatLng();
  var distance = currentLocation.distanceTo(map.getCenter());

  if (distance < 50) {
    document.getElementById("result").innerHTML = "<p class='success'>You have parked in the correct spot.</p>";
  } else {
    document.getElementById("result").innerHTML = "<p class='error'>You have not parked in the correct spot.</p>";
  }
}

document.getElementById("check-btn").addEventListener("click", checkParkingSpot);
