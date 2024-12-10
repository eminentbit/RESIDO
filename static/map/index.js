async function initMap() {
  // Import Map and AdvancedMarkerElement from the new API
  const { Map } = await google.maps.importLibrary("maps");
  const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");

  // Array to hold all markers
  let markers = [];

  // Map options
  const options = {
      center: { lat: 3.844119, lng: 11.50134 },
      zoom: 16,
      mapTypeId: 'terrain',
      mapId: 'YAOUNDE',
  };
  
  // Create a new map instance
  const map = new Map(document.getElementById("map"), options);
  
  const infoWindow = new google.maps.InfoWindow();
  
  // Add a marker when the map is clicked
  google.maps.event.addListener(map, 'click', (event) => {
      addMarker({ location: event.latLng });
  });

  // Function to add a marker to the map
  function addMarker(property) {
      // Create a new AdvancedMarkerElement instance
      const marker = new AdvancedMarkerElement({
          map: map,
          position: property.location,  // Correct position field instead of center
          title: property.content || '',  // Title or content for the marker
      });

      // Check for custom icon, and set as content in AdvancedMarkerElement
      if (property.icon) {
          const img = document.createElement('img');
          img.src = property.icon;
          marker.content = img;
      }

      // Handle info window for marker
      if (property.content) {
          const detailWindow = new google.maps.InfoWindow({
              content: property.content,
          });
          marker.addListener('mouseover', () => {
              detailWindow.open(map, marker);
          });

          marker.addListener('mouseout', () => {
              detailWindow.close();
          });
      }

      // Add a click event to remove the marker
      marker.addListener('click', () => {
          marker.setMap(null); // Remove marker from map
          markers = markers.filter(m => m !== marker); // Remove marker from array
      });

      // Add the marker to the markers array
      markers.push(marker);
  }

  // Add initial marker
  addMarker({
      location: { lat: 3.844119, lng: 11.50134 },
      icon: 'https://img.icons8.com/nolan/1.5x/marker.png',
      content: 'Yaounde',
  });

  const locationButton = document.getElementById('button');

  locationButton.textContent = "Pan to Current Location";
  locationButton.classList.add("custom-map-control-button");
  map.controls[google.maps.ControlPosition.TOP_CENTER].push(locationButton);

  locationButton.addEventListener("click", () => {
      // Try HTML5 geolocation.
      if (navigator.geolocation) {
          navigator.geolocation.getCurrentPosition(
              (position) => {
                  const pos = {
                      lat: position.coords.latitude,
                      lng: position.coords.longitude,
                  };

                  infoWindow.setOptions({
                    position: pos,
                    content: "You are here!",
                    pixelOffset: new google.maps.Size(0, -30) // Move the infoWindow upwards
                });
                  infoWindow.open(map);
                  map.setCenter(pos);
                  // Add marker for the current position
                  addMarker({
                      location: pos,
                      icon: 'https://img.icons8.com/ios-filled/50/000000/marker.png' // Custom icon for current location
                  });
              },
              () => {
                  handleLocationError(true, infoWindow, map.getCenter());
              },
          );
      } else {
          // Browser doesn't support Geolocation
          handleLocationError(false, infoWindow, map.getCenter());
      }
  });
}

// Handle geolocation error
function handleLocationError(browserHasGeolocation, infoWindow, pos) {
  infoWindow.setPosition(pos);
  infoWindow.setContent(
      browserHasGeolocation
          ? "Error: The Geolocation service failed."
          : "Error: Your browser doesn't support geolocation."
  );
  infoWindow.open(map);
}

window.initMap = initMap;
