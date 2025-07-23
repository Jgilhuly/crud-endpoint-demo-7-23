// Product CRUD Demo JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Add fade-in animation to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        card.classList.add('fade-in');
    });

    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // Price input formatting
    const priceInputs = document.querySelectorAll('input[name="price"]');
    priceInputs.forEach(input => {
        input.addEventListener('blur', function() {
            const value = parseFloat(this.value);
            if (!isNaN(value)) {
                this.value = value.toFixed(2);
            }
        });
    });

    // Tags input enhancement
    const tagsInputs = document.querySelectorAll('input[name="tags"]');
    tagsInputs.forEach(input => {
        input.addEventListener('input', function() {
            // Remove extra spaces and normalize commas
            this.value = this.value.replace(/\s*,\s*/g, ', ').replace(/,\s*,/g, ',');
        });
    });

    // Delete confirmation enhancement
    const deleteButtons = document.querySelectorAll('button[type="submit"]');
    deleteButtons.forEach(button => {
        if (button.textContent.trim() === 'Delete') {
            button.addEventListener('click', function(e) {
                const productName = this.closest('.card')?.querySelector('.card-title')?.textContent || 'this product';
                if (!confirm(`Are you sure you want to delete "${productName}"? This action cannot be undone.`)) {
                    e.preventDefault();
                }
            });
        }
    });

    // Auto-resize textareas
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(textarea => {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = this.scrollHeight + 'px';
        });
    });

    // Enhanced search functionality
    const searchInput = document.querySelector('#query');
    const quickSearchInput = document.querySelector('input[name="query"]');
    
    // Real-time search for quick search bar
    if (quickSearchInput && window.location.pathname === '/') {
        quickSearchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const cards = document.querySelectorAll('.product-card');
            
            cards.forEach(card => {
                const title = card.querySelector('.card-title')?.textContent.toLowerCase() || '';
                const description = card.querySelector('.card-text')?.textContent.toLowerCase() || '';
                const category = card.querySelector('.badge.bg-primary')?.textContent.toLowerCase() || '';
                const tags = Array.from(card.querySelectorAll('.badge.bg-secondary')).map(badge => badge.textContent.toLowerCase()).join(' ');
                
                if (title.includes(searchTerm) || 
                    description.includes(searchTerm) || 
                    category.includes(searchTerm) ||
                    tags.includes(searchTerm)) {
                    card.style.display = 'block';
                    card.style.opacity = '1';
                } else {
                    card.style.display = 'none';
                    card.style.opacity = '0.5';
                }
            });
            
            // Show/hide "no results" message
            const visibleCards = document.querySelectorAll('.product-card[style*="display: block"], .product-card:not([style*="display: none"])');
            updateResultsCounter(visibleCards.length);
        });
    }
    
    // Auto-submit search form on input changes (debounced)
    if (searchInput) {
        let searchTimeout;
        const form = searchInput.closest('form');
        
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                if (this.value.length >= 2 || this.value.length === 0) {
                    // Optional: auto-submit for better UX
                    // form.submit();
                }
            }, 500);
        });
    }

    // Toast notifications (if needed)
    function showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        toast.style.cssText = 'top: 20px; right: 20px; z-index: 1050; min-width: 300px;';
        toast.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        document.body.appendChild(toast);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (toast.parentNode) {
                toast.remove();
            }
        }, 5000);
    }

    // Expose showToast globally for potential use
    window.showToast = showToast;
    
    // Helper function to update results counter
    function updateResultsCounter(count) {
        const counter = document.querySelector('.results-counter');
        if (counter) {
            counter.textContent = `Found ${count} product(s)`;
        }
    }
    
    // API helper functions for search
    window.searchAPI = {
        async searchProducts(params) {
            const queryString = new URLSearchParams(params).toString();
            try {
                const response = await fetch(`/api/search?${queryString}`);
                return await response.json();
            } catch (error) {
                console.error('Search API error:', error);
                showToast('Search failed. Please try again.', 'danger');
                return [];
            }
        },
        
        async getCategories() {
            try {
                const response = await fetch('/api/categories');
                const data = await response.json();
                return data.categories;
            } catch (error) {
                console.error('Categories API error:', error);
                return [];
            }
        },
        
        async getTags() {
            try {
                const response = await fetch('/api/tags');
                const data = await response.json();
                return data.tags;
            } catch (error) {
                console.error('Tags API error:', error);
                return [];
            }
        }
    };
}); 