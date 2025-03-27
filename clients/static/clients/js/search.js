// Global variable to store client ID
let currentClientId = null;

// Handle search
document.addEventListener('DOMContentLoaded', function() {
    // Search button click handler
    document.getElementById('search-button').addEventListener('click', async function() {
        const documentType = document.getElementById('document-type').value;
        const documentNumber = document.getElementById('document-number').value;
        const errorMessage = document.getElementById('error-message');
        const resultContainer = document.getElementById('result-container');
        
        // Clear previous results
        errorMessage.textContent = '';
        errorMessage.classList.add('d-none');
        resultContainer.classList.add('d-none');
        
        // Validate inputs
        if (!documentType || !documentNumber) {
            errorMessage.textContent = 'Please select a document type and enter a document number.';
            errorMessage.classList.remove('d-none');
            return;
        }
        
        try {
            // Show loading state
            document.getElementById('search-button').disabled = true;
            document.getElementById('search-button').innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Searching...';
            
            // Make API request
            const response = await fetch(`/api/search-client/?document_type=${documentType}&document_number=${documentNumber}`);
            const data = await response.json();
            
            // Reset button state
            document.getElementById('search-button').disabled = false;
            document.getElementById('search-button').innerHTML = '<i class="bi bi-search me-1"></i> Search';
            
            if (response.ok) {
                // Display client data
                const client = data.client;
                currentClientId = client.id;
                
                document.getElementById('client-doc-type').textContent = client.document_type;
                document.getElementById('client-doc-number').textContent = client.document_number;
                document.getElementById('client-first-name').textContent = client.first_name;
                document.getElementById('client-last-name').textContent = client.last_name;
                document.getElementById('client-email').textContent = client.email;
                document.getElementById('client-phone').textContent = client.phone_number;
                document.getElementById('client-address').textContent = client.address;
                document.getElementById('client-city').textContent = client.city;
                
                resultContainer.classList.remove('d-none');
            } else {
                errorMessage.textContent = data.error || 'An error occurred while searching for the client.';
                errorMessage.classList.remove('d-none');
            }
        } catch (error) {
            document.getElementById('search-button').disabled = false;
            document.getElementById('search-button').innerHTML = '<i class="bi bi-search me-1"></i> Search';
            
            errorMessage.textContent = 'An error occurred while connecting to the server.';
            errorMessage.classList.remove('d-none');
            console.error('Error:', error);
        }
    });
    
    // Export buttons
    document.getElementById('export-csv').addEventListener('click', function() {
        if (currentClientId) {
            window.location.href = `/export-client/${currentClientId}/csv/`;
        }
    });
    
    document.getElementById('export-excel').addEventListener('click', function() {
        if (currentClientId) {
            window.location.href = `/export-client/${currentClientId}/excel/`;
        }
    });
    
    document.getElementById('export-txt').addEventListener('click', function() {
        if (currentClientId) {
            window.location.href = `/export-client/${currentClientId}/txt/`;
        }
    });
}); 