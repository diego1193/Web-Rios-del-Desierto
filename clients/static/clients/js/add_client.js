document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('add-client-form');
    
    form.addEventListener('submit', function(e) {
        let isValid = true;
        const requiredFields = form.querySelectorAll('[required]');
        
        // Clear previous validation errors
        form.querySelectorAll('.is-invalid').forEach(field => {
            field.classList.remove('is-invalid');
        });
        
        // Check required fields
        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                field.classList.add('is-invalid');
                isValid = false;
            }
        });
        
        // Email validation
        const emailField = document.getElementById('email');
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (emailField.value.trim() && !emailRegex.test(emailField.value.trim())) {
            emailField.classList.add('is-invalid');
            isValid = false;
        }
        
        // Phone validation (basic)
        const phoneField = document.getElementById('phone_number');
        const phoneRegex = /^[0-9+\-\s()]{7,15}$/;
        if (phoneField.value.trim() && !phoneRegex.test(phoneField.value.trim())) {
            phoneField.classList.add('is-invalid');
            isValid = false;
        }
        
        if (!isValid) {
            e.preventDefault();
            // Scroll to first invalid field
            const firstInvalid = form.querySelector('.is-invalid');
            if (firstInvalid) {
                firstInvalid.scrollIntoView({ behavior: 'smooth', block: 'center' });
                firstInvalid.focus();
            }
        }
    });
}); 