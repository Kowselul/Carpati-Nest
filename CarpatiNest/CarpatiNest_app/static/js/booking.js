// Main booking form handling with confirmation modal
document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM fully loaded - initializing booking form handler");
    
    // Get DOM elements
    const form = document.getElementById('bookingForm');
    const submitButton = document.getElementById('submitButton');
    const modal = document.getElementById('confirmationModal');
    const confirmButton = document.getElementById('confirmBooking');
    const cancelButton = document.getElementById('cancelBooking');
    const closeButton = document.getElementById('closeModal');
    
    // Global form state
    const refugeId = form ? form.getAttribute('data-refuge-id') : null;
    const formId = form ? form.querySelector('[name="form_submitted"]').value : null;
    const submittedKey = refugeId && formId ? `booking_form_${refugeId}_${formId}` : null;
    const currentDate = new Date().toISOString().split('T')[0]; // Format YYYY-MM-DD
    let isSubmitting = false;
    
    console.log("Form elements:", {
        form: !!form,
        submitButton: !!submitButton,
        modal: !!modal,
        confirmButton: !!confirmButton,
        refugeId: refugeId,
        formId: formId && formId.substring(0, 20) + "..."
    });
    
    // Clean up old session storage items
    Object.keys(sessionStorage).forEach(key => {
        if (key.startsWith('booking_form_') && key.includes(currentDate) === false) {
            sessionStorage.removeItem(key);
        }
    });
    
    // Modal handling functions
    function showModal() {
        if (!modal) return;
        
        console.log("Showing confirmation modal");
        modal.style.display = 'flex';
        setTimeout(() => {
            modal.classList.add('visible');
        }, 10);
    }
    
    function closeModal() {
        if (!modal) return;
        
        console.log("Closing confirmation modal");
        modal.classList.remove('visible');
        setTimeout(() => {
            modal.style.display = 'none';
        }, 300);
    }
    
    // Toast message function
    function showToast(message, type) {
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.innerHTML = `
            <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i>
            <span>${message}</span>
        `;
        document.querySelector('.toast-container').appendChild(toast);
        
        setTimeout(() => {
            toast.remove();
        }, 5000);
    }
      // CSRF token retrieval - improved to be more robust
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        
        // If cookie is not found, try getting it from the form
        if (!cookieValue && document.querySelector('[name="csrfmiddlewaretoken"]')) {
            cookieValue = document.querySelector('[name="csrfmiddlewaretoken"]').value;
            console.log("Got CSRF token from form field");
        }
        
        return cookieValue;
    }      // Form submission function - improved with better error handling
    async function submitFormData() {
        console.log("Starting form submission process...");
        
        if (!form) {
            console.error("Can't submit: form not found");
            showToast('Formular negăsit. Reîmprospătați pagina și încercați din nou.', 'error');
            return;
        }
        
        // Block multiple submissions
        if (isSubmitting) {
            console.log('Form is already being submitted. Ignoring.');
            return false;
        }
        
        // Check if all required fields are filled
        const bookingDate = form.querySelector('[name="booking_date"]').value;
        const membersCount = form.querySelector('[name="members_count"]').value;
        
        if (!bookingDate || !membersCount) {
            console.error("Missing required fields:", { bookingDate, membersCount });
            showToast('Completați toate câmpurile obligatorii.', 'error');
            return false;
        }
        
        // Set submission flag
        isSubmitting = true;
        
        // Update UI to show loading state
        if (submitButton) {
            submitButton.classList.add('loading');
            submitButton.setAttribute('disabled', 'disabled');
            submitButton.innerHTML = '<i class="fas fa-circle-notch fa-spin"></i> Se procesează...';
        }
        
        // Disable all form fields to prevent changes during submission
        Array.from(form.elements).forEach(element => {
            if (element !== submitButton) { // We've already disabled the submit button
                element.setAttribute('disabled', 'disabled');
            }
        });
        
        try {
            console.log("Preparing form data...");
            const csrftoken = getCookie('csrftoken');
            console.log("CSRF Token:", csrftoken ? "Token found" : "Token missing");
            
            const formData = new FormData(form);
            const bookingDate = formData.get('booking_date');
            const membersCount = formData.get('members_count');
            console.log("Form data check:", { bookingDate, membersCount });
            
            if (!bookingDate || !membersCount) {
                throw new Error('Lipsesc câmpuri obligatorii. Asigurați-vă că ați selectat data rezervării și numărul de membri.');
            }
            
            console.log("Sending AJAX request...");
            // Send form via AJAX
            console.log("Full Headers being sent:", {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrftoken ? csrftoken.substring(0, 5) + "..." : "missing",
                'X-Form-Submit-Type': 'ajax',
                'Content-Type': 'multipart/form-data'
            });
              // Make sure the CSRF token is included in the form data as well
            if (csrftoken && !formData.has('csrfmiddlewaretoken')) {
                formData.append('csrfmiddlewaretoken', csrftoken);
                console.log("Added CSRF token to form data");
            }
            
            const response = await fetch(window.location.href, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrftoken,
                    'X-Form-Submit-Type': 'ajax'
                },
                credentials: 'same-origin'
            });
            
            console.log("Response received:", response.status, response.statusText);
            console.log("Response headers:", Object.fromEntries([...response.headers.entries()]));
            const contentType = response.headers.get("content-type");
            
            if (contentType && contentType.includes("application/json")) {
                const result = await response.json();
                console.log("JSON response:", result);
                
                if (response.ok) {
                    showToast('Rezervarea a fost înregistrată cu succes!', 'success');
                    
                    if (result.available_spots !== undefined) {
                        document.getElementById('available-spots-count').textContent = result.available_spots;
                    }
                      // Improve redirect handling - both for with and without URL
                    if (result.redirect_url) {
                        console.log("Redirecting to:", result.redirect_url);
                        // Store success in session storage
                        sessionStorage.setItem('booking_success', 'true');
                        sessionStorage.setItem('redirected', 'true');
                        
                        // Force a direct location change instead of delayed
                        window.location.href = result.redirect_url;
                    } else {
                        console.log("No redirect URL provided, reloading page");
                        // If no redirect URL is provided, still try to find the booking ID
                        if (result.booking_id) {
                            const confirmUrl = `/booking/confirmation/${result.booking_id}/`;
                            console.log("Generated confirmation URL:", confirmUrl);
                            window.location.href = confirmUrl;
                        } else {
                            // Last resort - reload the page
                            setTimeout(() => {
                                location.reload();
                            }, 1000);
                        }
                    }
                } else {
                    resetFormState();
                    
                    if (result.errors) {
                        console.log("Validation errors:", result.errors);
                        for (const field in result.errors) {
                            if (result.errors.hasOwnProperty(field)) {
                                result.errors[field].forEach(message => {
                                    showToast(`${field}: ${message}`, 'error');
                                });
                            }
                        }
                    } else {
                        showToast(result.error || 'A apărut o eroare. Vă rugăm să încercați din nou.', 'error');
                    }
                }
            } else {
                window.location.href = response.url;
            }
        } catch (error) {
            console.error('Error submitting form:', error);
            resetFormState();
            showToast('A apărut o eroare la comunicarea cu serverul. Vă rugăm să încercați din nou.', 'error');
        }
    }
    
    function resetFormState() {
        sessionStorage.removeItem(submittedKey);
        isSubmitting = false;
        
        if (submitButton) {
            submitButton.classList.remove('loading');
            submitButton.removeAttribute('disabled');
        }
        
        Array.from(form.elements).forEach(element => {
            element.removeAttribute('disabled');
        });
    }
    
    // Event handlers
    if (form) {
        console.log("Setting up form event handler");
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Update modal content with form data
            const bookingDate = form.querySelector('#id_booking_date_alt').value;
            const membersCount = form.querySelector('#id_members_count').value;
            const refugePrice = form.getAttribute('data-refuge-price') || 0;
            const totalCost = membersCount * refugePrice;
            
            if (document.getElementById('confirmDate')) {
                document.getElementById('confirmDate').textContent = bookingDate;
            }
            if (document.getElementById('confirmPersons')) {
                document.getElementById('confirmPersons').textContent = membersCount;
            }
            if (document.getElementById('confirmTotalCost')) {
                document.getElementById('confirmTotalCost').textContent = totalCost + ' RON';
            }
            
            showModal();
        });
    }      if (confirmButton) {
        console.log("Setting up confirm button event handler");
        confirmButton.addEventListener('click', async function(event) {
            event.preventDefault(); // Prevent any default action
            console.log("Confirm button clicked!");
            
            // Disable the button to prevent multiple clicks
            confirmButton.disabled = true;
            confirmButton.innerHTML = '<i class="fas fa-circle-notch fa-spin"></i> Se procesează...';
            
            try {
                // First close the modal with animation
                closeModal();
                
                // Wait for modal to close before submitting
                setTimeout(async () => {
                    console.log("Modal closed, now submitting form data");
                    try {
                        await submitFormData();
                    } catch (error) {
                        console.error("Error during form submission:", error);
                        showToast("A apărut o eroare. Te rugăm să încerci din nou.", "error");
                        resetFormState();
                        // Re-enable the button in case of error
                        confirmButton.disabled = false;
                        confirmButton.innerHTML = 'Confirmă rezervarea';
                    }
                }, 310); // Just after modal closing animation completes
            } catch (error) {
                console.error("Error in confirmation flow:", error);
                showToast("A apărut o eroare. Te rugăm să încerci din nou.", "error");
                resetFormState();
                // Re-enable the button in case of error
                confirmButton.disabled = false;
                confirmButton.innerHTML = 'Confirmă rezervarea';
            }
        });
    }
    
    if (cancelButton) {
        cancelButton.addEventListener('click', closeModal);
    }
    
    if (closeButton) {
        closeButton.addEventListener('click', closeModal);
    }
    
    if (modal) {
        modal.addEventListener('click', function(event) {
            if (event.target === modal) {
                closeModal();
            }
        });
    }
});
