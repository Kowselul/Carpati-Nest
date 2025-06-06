// Flatpickr and availability checker
document.addEventListener('DOMContentLoaded', function() {
    console.log("Initializing date picker and availability checker");
    
    // Initialize flatpickr
    const datePickr = flatpickr(".flatpickr", {
        locale: "ro",
        dateFormat: "Y-m-d",
        minDate: "today",
        disableMobile: "true",
        altInput: true,
        altFormat: "j F Y",
        monthSelectorType: "static",
        animate: true,
        defaultDate: "today", // Default to today to avoid validation errors
        onChange: function(selectedDates, dateStr, instance) {
            // Check availability for selected date
            checkAvailability(dateStr);
            console.log("Selected date:", dateStr);
        }
    });
    
    // Check availability for default date (today)
    if (datePickr && datePickr.length > 0) {
        const today = new Date().toISOString().split('T')[0];
        checkAvailability(today);
        console.log("Checking availability for today:", today);
    }
      
    // Function to check availability for selected date
    async function checkAvailability(date) {
        try {
            // Get refuge ID from form data attribute
            const form = document.getElementById('bookingForm');
            const refugeId = form ? form.getAttribute('data-refuge-id') : null;
            
            if (!refugeId) {
                console.error("Could not find refuge ID");
                return;
            }
            
            const response = await fetch(`/api/check-availability/?refuge_id=${refugeId}&date=${date}`);
            const data = await response.json();
            
            if(response.ok) {
                // Update displayed available spots
                const availableSpotsElement = document.getElementById('available-spots-count');
                if (availableSpotsElement) {
                    availableSpotsElement.textContent = data.available_spots;
                }
                
                // Update availability message
                const membersInput = document.querySelector('#id_members_count');
                const formHint = document.querySelector('.form-hint');
                
                if (!membersInput || !formHint) {
                    console.error("Could not find members input or form hint elements");
                    return;
                }
                          if (data.available_spots <= 0) {
                    formHint.textContent = 'Nu mai sunt locuri disponibile pentru această dată!';
                    formHint.style.color = '#e53e3e';
                    membersInput.setAttribute('disabled', 'disabled');
                } else {
                    formHint.textContent = `Maxim ${data.available_spots} persoane disponibile`;
                    formHint.style.color = '';
                    membersInput.removeAttribute('disabled');
                    membersInput.setAttribute('max', data.available_spots);
                    
                    // Update value if it's higher than availability
                    if (parseInt(membersInput.value) > data.available_spots) {
                        membersInput.value = data.available_spots;
                    }
                }
                
                // Check weather for selected date if weather service is available
                if (window.weatherService && refugeId) {
                    window.weatherService.checkWeatherForDate(refugeId, date);
                }
            }
        } catch (error) {
            console.error('Error checking availability:', error);
        }
    }
    
    // Scroll to reviews functionality
    const scrollToReviews = document.querySelector('.scroll-to-reviews');
    if (scrollToReviews) {
        scrollToReviews.addEventListener('click', function(e) {
            e.preventDefault();
            
            const reviewsSection = document.getElementById('reviews');
            if (reviewsSection) {
                reviewsSection.scrollIntoView({ 
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    }
});
