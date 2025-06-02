document.addEventListener('DOMContentLoaded', function() {
    // User dropdown functionality
    const userDropdown = document.querySelector('.user-dropdown');
    const userButton = document.querySelector('.user-button');

    if (userButton && userDropdown) {
        // Toggle dropdown on button click
        userButton.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            userDropdown.classList.toggle('active');
        });

        // Close dropdown when clicking outside
        document.addEventListener('click', function(e) {
            if (!userDropdown.contains(e.target)) {
                userDropdown.classList.remove('active');
            }
        });

        // Close dropdown when pressing Escape key
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                userDropdown.classList.remove('active');
            }
        });
    }

    // Smooth scroll pentru link-ul "Începe Aventura"
    const adventureLink = document.querySelector('a[href="#about"]');
    if (adventureLink) {
        adventureLink.addEventListener("click", function (e) {
            e.preventDefault();
            document.querySelector("#about").scrollIntoView({
                behavior: "smooth",
            });
        });
    }

    // Navbar visibility
    const navbar = document.getElementById("navbar");
    if (navbar) {
        window.addEventListener("scroll", function () {
            if (window.scrollY > 100) {
                navbar.classList.add("visible");
            } else {
                navbar.classList.remove("visible");
            }
        });

        // Show navbar initially
        navbar.classList.add('visible');
    }
});
