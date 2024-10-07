// Load Google Maps API with the Places library
$.getScript(`https://maps.googleapis.com/maps/api/js?key=${google_api_key}&libraries=places`)
    .done(function() {
        window.addEventListener('load', initAutoComplete);  // Use modern event listener
    })
    .fail(function(jqxhr, settings, exception) {
        console.error("Failed to load Google Maps script: ", exception);
    });

let autocomplete;

// Initialize Autocomplete
function initAutoComplete() {
    autocomplete = new google.maps.places.Autocomplete(
        document.getElementById('id-google-address'),
        {
            types: ['address'],  // Suggest only addresses
            componentRestrictions: { country: ['us', 'ca'] }  // Restrict to US and Canada
        }
    );

    autocomplete.addListener('place_changed', onPlaceChanged);  // Use addListener for event handling
}

// On place selection
function onPlaceChanged() {
    const place = autocomplete.getPlace();  // Get the place object from Google Places API

    // Check if place has geometry (location)
    if (!place.geometry) {
        document.getElementById('id-google-address').placeholder = "*Begin typing address";
        return;  // Exit if no valid place was selected
    }

    // Initialize Geocoder for additional geocode handling
    const geocoder = new google.maps.Geocoder();
    const address = document.getElementById('id-google-address').value;
    console.log(address);

    // Use Geocoder to get latitude and longitude
    geocoder.geocode({ address: address }, function(results, status) {
        if (status === google.maps.GeocoderStatus.OK) {
            const latitude = results[0].geometry.location.lat();
            const longitude = results[0].geometry.location.lng();

            // Populate the hidden form fields with lat and lng
            document.getElementById('id_longitude').value = longitude;
            document.getElementById('id_latitude').value = latitude;

            console.log("Latitude:", latitude, "Longitude:", longitude);  // For debugging
        } else {
            console.error("Geocoder failed:", status);
        }
    });

    // Variables to store address components
    let num = "";
    let addy = "";

    // Loop through the address components and assign values
    place.address_components.forEach(component => {
        if (component.types.includes("street_number")) {
            num = component.long_name;  // Street number
        }
        if (component.types.includes("route")) {
            addy = component.long_name;  // Street name
        }
        if (component.types.includes("locality")) {
            document.getElementById('id_town').value = component.long_name;  // Town/City
        }
        if (component.types.includes("country")) {
            document.getElementById('id_country').value = component.long_name;  // Country
        }
        if (component.types.includes("postal_code")) {
            document.getElementById('id_post_code').value = component.long_name;  // Postal code
        }
    });

    // Combine street number and street name and update address field
    document.getElementById('id_address').value = `${num} ${addy}`;

    // Find all hidden input fields and make them visible except CSRF token
    document.querySelectorAll("input[type='hidden']").forEach(input => {
        if (input.name !== "csrfmiddlewaretoken") {
            input.type = "text";  // Change the type from hidden to text
            input.classList.remove('hidden-el');  // Remove the hidden class
        }
    });

    // Fade in the now completed form and enable the submit button
    document.querySelectorAll('.hidden-el').forEach(el => {
        el.style.display = 'block';
    });
    document.getElementById('profile-btn').removeAttribute("disabled");
}

// Disable the submit button if input is cleared
document.getElementById('id-google-address').addEventListener('input', function() {
    if (!this.value) {
        document.getElementById('profile-btn').setAttribute("disabled", true);  // Disable button if input is empty
    }
});