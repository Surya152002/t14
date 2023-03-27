// Leaflet map initialization
var map = L.map('mapid').setView([51.505, -0.09], 13);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
    maxZoom: 18
}).addTo(map);

// Parking slot location (latitude, longitude)
var parkingSlot = L.latLng(51.505, -0.09);

// Check parking function
function checkParking() {
	// Get user location using geolocation
	navigator.geolocation.getCurrentPosition(function(position) {
		var userLocation = L.latLng(position.coords.latitude, position.coords.longitude);
		// Calculate distance between user location and parking slot
		var distance = userLocation.distanceTo(parkingSlot);
		// If distance is less than 10 meters, the user is parked in the correct slot
		if (distance < 10) {
			alert("You are parked in the correct slot!");
		} else {
			alert("You are not parked in the correct slot. Please move your vehicle.");
		}
	}, function() {
		alert("Unable to retrieve your location.");
	});
}
