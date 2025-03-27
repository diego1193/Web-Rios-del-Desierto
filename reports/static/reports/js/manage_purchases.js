document.addEventListener('DOMContentLoaded', function() {
    const clientSearch = document.getElementById('client_search');
    const searchClientBtn = document.getElementById('search_client_btn');
    const clientSelect = document.getElementById('client_id');
    const clientIdActual = document.getElementById('client_id_actual');
    
    // Handle client search
    searchClientBtn.addEventListener('click', async function() {
        const searchTerm = clientSearch.value.trim();
        if (!searchTerm) {
            alert('Please enter a search term');
            return;
        }
        
        try {
            const response = await fetch(`/api/search-clients/?term=${encodeURIComponent(searchTerm)}`);
            const data = await response.json();
            
            // Clear previous options
            clientSelect.innerHTML = '<option value="">Select a client</option>';
            
            if (response.ok && data.clients && data.clients.length > 0) {
                // Add client options
                data.clients.forEach(client => {
                    const option = document.createElement('option');
                    option.value = client.id;
                    option.textContent = `${client.first_name} ${client.last_name} - ${client.document_type} ${client.document_number}`;
                    clientSelect.appendChild(option);
                });
                
                // Enable select
                clientSelect.disabled = false;
            } else {
                alert('No clients found matching your search term.');
                clientSelect.disabled = true;
            }
        } catch (error) {
            console.error('Error searching for clients:', error);
            alert('An error occurred while searching for clients.');
        }
    });
    
    // Handle client selection
    clientSelect.addEventListener('change', function() {
        clientIdActual.value = this.value;
    });
    
    // Set today's date as default
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('purchase_date').value = today;
    
    // Form validation
    const purchaseForm = document.getElementById('purchase-form');
    if (purchaseForm) {
        purchaseForm.addEventListener('submit', function(e) {
            if (!clientIdActual.value) {
                e.preventDefault();
                alert('Please select a client.');
            }
        });
    }
    
    // Format amount input
    const amountInput = document.getElementById('amount');
    if (amountInput) {
        // Format number when leaving the field
        amountInput.addEventListener('blur', function() {
            if (this.value) {
                // Remove any non-digit characters
                const numericValue = this.value.replace(/[^\d]/g, '');
                if (numericValue) {
                    // Format with thousand separators
                    this.value = parseInt(numericValue).toLocaleString('es-CO');
                }
            }
        });
        
        // Clean formatting when focusing on the field
        amountInput.addEventListener('focus', function() {
            // Remove any non-digit characters for editing
            this.value = this.value.replace(/[^\d]/g, '');
        });
        
        // Only allow numeric input while typing
        amountInput.addEventListener('input', function(e) {
            // Temporary allow digits and commas while typing
            this.value = this.value.replace(/[^\d,]/g, '');
        });
    }

    // Handle tab persistence with pagination
    const urlParams = new URLSearchParams(window.location.search);
    const tabParam = urlParams.get('tab');

    if (tabParam === 'bulk') {
        // Show bulk tab
        const bulkTab = document.getElementById('bulk-tab');
        if (bulkTab) {
            const tab = new bootstrap.Tab(bulkTab);
            tab.show();
        }
    }

    // Add tab parameter to pagination links if needed
    document.querySelectorAll('.pagination .page-link').forEach(link => {
        const activeTab = document.querySelector('.nav-tabs .active');
        if (activeTab && activeTab.id === 'bulk-tab' && !link.href.includes('tab=')) {
            if (link.href.includes('?')) {
                link.href += '&tab=bulk';
            } else {
                link.href += '?tab=bulk';
            }
        }
    });
}); 