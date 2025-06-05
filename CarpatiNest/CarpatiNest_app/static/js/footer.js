// Footer Newsletter Form
document.addEventListener('DOMContentLoaded', function() {
    const newsletterForm = document.querySelector('.newsletter-form');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const emailInput = this.querySelector('.newsletter-input');
            const email = emailInput.value.trim();
            
            if (validateEmail(email)) {
                // Aici ar trebui să fie codul pentru a trimite emailul către server
                // Pentru moment, vom afișa doar un mesaj de succes
                
                // Creăm un element pentru mesajul de succes
                const successMessage = document.createElement('div');
                successMessage.className = 'newsletter-success';
                successMessage.innerHTML = '<i class="fas fa-check-circle"></i> Te-ai abonat cu succes!';
                successMessage.style.color = '#4ade80';
                successMessage.style.marginTop = '10px';
                successMessage.style.fontSize = '14px';
                successMessage.style.fontWeight = '500';
                successMessage.style.display = 'flex';
                successMessage.style.alignItems = 'center';
                
                // Adăugăm un pic de spațiu între icoană și text
                successMessage.querySelector('i').style.marginRight = '5px';
                
                // Verificăm dacă există deja un mesaj de succes sau eroare și îl ștergem
                const existingMessage = newsletterForm.querySelector('.newsletter-success, .newsletter-error');
                if (existingMessage) {
                    existingMessage.remove();
                }
                
                // Adăugăm mesajul după formular
                newsletterForm.appendChild(successMessage);
                
                // Resetăm formularul
                emailInput.value = '';
                
                // Ascundem mesajul după 3 secunde
                setTimeout(() => {
                    successMessage.style.opacity = '0';
                    successMessage.style.transition = 'opacity 0.5s ease';
                    
                    setTimeout(() => {
                        successMessage.remove();
                    }, 500);
                }, 3000);
            } else {
                // Creăm un element pentru mesajul de eroare
                const errorMessage = document.createElement('div');
                errorMessage.className = 'newsletter-error';
                errorMessage.innerHTML = '<i class="fas fa-exclamation-circle"></i> Te rugăm să introduci o adresă de email validă.';
                errorMessage.style.color = '#e53e3e';
                errorMessage.style.marginTop = '10px';
                errorMessage.style.fontSize = '14px';
                errorMessage.style.fontWeight = '500';
                errorMessage.style.display = 'flex';
                errorMessage.style.alignItems = 'center';
                
                // Adăugăm un pic de spațiu între icoană și text
                errorMessage.querySelector('i').style.marginRight = '5px';
                
                // Verificăm dacă există deja un mesaj de succes sau eroare și îl ștergem
                const existingMessage = newsletterForm.querySelector('.newsletter-success, .newsletter-error');
                if (existingMessage) {
                    existingMessage.remove();
                }
                
                // Adăugăm mesajul după formular
                newsletterForm.appendChild(errorMessage);
                
                // Ascundem mesajul după 3 secunde
                setTimeout(() => {
                    errorMessage.style.opacity = '0';
                    errorMessage.style.transition = 'opacity 0.5s ease';
                    
                    setTimeout(() => {
                        errorMessage.remove();
                    }, 500);
                }, 3000);
            }
        });
    }
    
    // Funcție pentru validarea emailului
    function validateEmail(email) {
        const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return re.test(email);
    }
});
