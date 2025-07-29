// BookSwapBuddy JavaScript - Enhanced functionality and user experience

document.addEventListener('DOMContentLoaded', function() {
    
    // Initialize all components
    initializeSearchFilters();
    initializeFormValidation();
    initializeImagePreviews();
    initializeMessageSystem();
    initializeQRCodeDisplay();
    initializeTooltips();
    initializeAutocomplete();
    initializePriceToggle();
    
    console.log('BookSwapBuddy JavaScript initialized successfully!');
});

// Search and Filter Functions
function initializeSearchFilters() {
    const searchForm = document.getElementById('search-form');
    const filterInputs = document.querySelectorAll('.filter-input');
    
    if (searchForm) {
        // Real-time search
        const searchInput = document.getElementById('search-input');
        if (searchInput) {
            let searchTimeout;
            searchInput.addEventListener('input', function() {
                clearTimeout(searchTimeout);
                searchTimeout = setTimeout(() => {
                    updateSearchResults();
                }, 500);
            });
        }
        
        // Filter change handlers
        filterInputs.forEach(input => {
            input.addEventListener('change', updateSearchResults);
        });
    }
    
    // Clear filters button
    const clearFiltersBtn = document.getElementById('clear-filters');
    if (clearFiltersBtn) {
        clearFiltersBtn.addEventListener('click', function() {
            filterInputs.forEach(input => {
                if (input.type === 'select-one') {
                    input.selectedIndex = 0;
                } else {
                    input.value = '';
                }
            });
            updateSearchResults();
        });
    }
}

function updateSearchResults() {
    const formData = new FormData(document.getElementById('search-form'));
    const params = new URLSearchParams(formData);
    
    // Show loading indicator
    showLoadingIndicator();
    
    // Update URL without page reload
    const newUrl = `${window.location.pathname}?${params.toString()}`;
    window.history.pushState({}, '', newUrl);
    
    // Fetch updated results
    fetch(`/api/books?${params.toString()}`)
        .then(response => response.json())
        .then(data => {
            updateBookGrid(data.books);
            updatePagination(data.pagination);
            hideLoadingIndicator();
        })
        .catch(error => {
            console.error('Error fetching search results:', error);
            hideLoadingIndicator();
            showNotification('Error loading search results. Please try again.', 'error');
        });
}

function updateBookGrid(books) {
    const bookGrid = document.getElementById('book-grid');
    if (!bookGrid) return;
    
    if (books.length === 0) {
        bookGrid.innerHTML = `
            <div class="col-12 text-center">
                <div class="card">
                    <div class="card-body">
                        <h5>No books found</h5>
                        <p class="text-muted">Try adjusting your search criteria or browse all books.</p>
                        <a href="/books" class="btn btn-primary">Browse All Books</a>
                    </div>
                </div>
            </div>
        `;
        return;
    }
    
    bookGrid.innerHTML = books.map(book => createBookCard(book)).join('');
}

function createBookCard(book) {
    const imageUrl = book.image_filename ? `/static/uploads/${book.image_filename}` : '/static/images/default-book.png';
    const priceDisplay = book.swap_type === 'free' ? 'FREE' : 
                        book.swap_type === 'swap' ? 'SWAP' : `₹${book.price}`;
    
    return `
        <div class="col-lg-4 col-md-6 col-sm-12 mb-4">
            <div class="card book-card h-100">
                <img src="${imageUrl}" class="card-img-top" alt="${book.title}" 
                     onerror="this.src='/static/images/default-book.png'">
                <div class="card-body d-flex flex-column">
                    <h5 class="card-title">${escapeHtml(book.title)}</h5>
                    <p class="card-text text-muted">by ${escapeHtml(book.author)}</p>
                    <p class="card-text">${escapeHtml(book.subject)}</p>
                    <div class="mt-auto">
                        <div class="d-flex justify-content-between align-items-center mb-2">
                            <span class="book-price">${priceDisplay}</span>
                            <span class="badge condition-${book.condition.toLowerCase().replace(' ', '-')}">${book.condition}</span>
                        </div>
                        <div class="d-flex justify-content-between align-items-center">
                            <span class="badge swap-${book.swap_type}">${book.swap_type.toUpperCase()}</span>
                            <a href="/book/${book.id}" class="btn btn-primary btn-sm">View Details</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

// Form Validation
function initializeFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
                
                // Focus on first invalid field
                const firstInvalid = form.querySelector(':invalid');
                if (firstInvalid) {
                    firstInvalid.focus();
                    showNotification('Please fill in all required fields correctly.', 'warning');
                }
            }
            
            form.classList.add('was-validated');
        });
        
        // Real-time validation
        const inputs = form.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                validateField(input);
            });
            
            input.addEventListener('input', function() {
                if (input.classList.contains('is-invalid')) {
                    validateField(input);
                }
            });
        });
    });
    
    // Password confirmation validation
    const passwordField = document.getElementById('password');
    const confirmPasswordField = document.getElementById('confirm_password');
    
    if (passwordField && confirmPasswordField) {
        confirmPasswordField.addEventListener('input', function() {
            if (passwordField.value !== confirmPasswordField.value) {
                confirmPasswordField.setCustomValidity('Passwords do not match');
            } else {
                confirmPasswordField.setCustomValidity('');
            }
        });
    }
}

function validateField(field) {
    const isValid = field.checkValidity();
    
    field.classList.remove('is-valid', 'is-invalid');
    field.classList.add(isValid ? 'is-valid' : 'is-invalid');
    
    // Custom validation messages
    const feedback = field.parentNode.querySelector('.invalid-feedback');
    if (feedback && !isValid) {
        if (field.validity.valueMissing) {
            feedback.textContent = 'This field is required.';
        } else if (field.validity.typeMismatch) {
            feedback.textContent = 'Please enter a valid value.';
        } else if (field.validity.patternMismatch) {
            feedback.textContent = 'Please match the requested format.';
        }
    }
}

// Image Preview and Upload
function initializeImagePreviews() {
    const imageInputs = document.querySelectorAll('input[type="file"][accept*="image"]');
    
    imageInputs.forEach(input => {
        input.addEventListener('change', function(event) {
            const file = event.target.files[0];
            const previewContainer = document.getElementById(input.id + '-preview');
            
            if (file && previewContainer) {
                // Validate file size (16MB max)
                if (file.size > 16 * 1024 * 1024) {
                    showNotification('File size must be less than 16MB.', 'error');
                    input.value = '';
                    return;
                }
                
                // Validate file type
                if (!file.type.startsWith('image/')) {
                    showNotification('Please select a valid image file.', 'error');
                    input.value = '';
                    return;
                }
                
                const reader = new FileReader();
                reader.onload = function(e) {
                    previewContainer.innerHTML = `
                        <img src="${e.target.result}" class="img-fluid rounded" 
                             style="max-height: 200px; width: auto;" alt="Preview">
                        <button type="button" class="btn btn-sm btn-danger mt-2" onclick="clearImagePreview('${input.id}')">
                            Remove Image
                        </button>
                    `;
                };
                reader.readAsDataURL(file);
            }
        });
    });
}

function clearImagePreview(inputId) {
    const input = document.getElementById(inputId);
    const preview = document.getElementById(inputId + '-preview');
    
    if (input) input.value = '';
    if (preview) preview.innerHTML = '';
}

// Message System
function initializeMessageSystem() {
    const messageForm = document.getElementById('message-form');
    if (messageForm) {
        messageForm.addEventListener('submit', function(event) {
            event.preventDefault();
            sendMessage();
        });
    }
    
    // Auto-expand textarea
    const messageTextarea = document.getElementById('message-content');
    if (messageTextarea) {
        messageTextarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = this.scrollHeight + 'px';
        });
    }
    
    // Mark messages as read when viewed
    markMessagesAsRead();
}

function sendMessage() {
    const form = document.getElementById('message-form');
    const formData = new FormData(form);
    
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    submitBtn.textContent = 'Sending...';
    submitBtn.disabled = true;
    
    fetch('/send_message', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            showNotification('Message sent successfully!', 'success');
            form.reset();
            // Optionally refresh messages
            if (window.location.pathname === '/messages') {
                setTimeout(() => window.location.reload(), 1000);
            }
        } else {
            throw new Error('Failed to send message');
        }
    })
    .catch(error => {
        console.error('Error sending message:', error);
        showNotification('Failed to send message. Please try again.', 'error');
    })
    .finally(() => {
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
    });
}

function markMessagesAsRead() {
    const messageItems = document.querySelectorAll('.message-item[data-message-id]');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const messageId = entry.target.dataset.messageId;
                if (messageId) {
                    markMessageAsRead(messageId);
                    observer.unobserve(entry.target);
                }
            }
        });
    });
    
    messageItems.forEach(item => observer.observe(item));
}

function markMessageAsRead(messageId) {
    fetch(`/api/messages/${messageId}/read`, {
        method: 'POST'
    }).catch(error => console.error('Error marking message as read:', error));
}

// QR Code Display
function initializeQRCodeDisplay() {
    const qrCodeBtns = document.querySelectorAll('.show-qr-btn');
    
    qrCodeBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const bookId = this.dataset.bookId;
            showQRCode(bookId);
        });
    });
}

function showQRCode(bookId) {
    fetch(`/api/book/${bookId}/qr`)
        .then(response => response.json())
        .then(data => {
            const modal = document.getElementById('qrModal') || createQRModal();
            const modalBody = modal.querySelector('.modal-body');
            
            modalBody.innerHTML = `
                <div class="text-center">
                    <h5>QR Code for Book Exchange</h5>
                    <img src="${data.qr_code}" alt="QR Code" class="qr-code mb-3">
                    <p class="text-muted">Show this QR code during the book exchange to verify authenticity.</p>
                    <button type="button" class="btn btn-primary" onclick="downloadQRCode('${data.qr_code}', '${data.book_title}')">
                        Download QR Code
                    </button>
                </div>
            `;
            
            const bootstrapModal = new bootstrap.Modal(modal);
            bootstrapModal.show();
        })
        .catch(error => {
            console.error('Error loading QR code:', error);
            showNotification('Failed to load QR code. Please try again.', 'error');
        });
}

function createQRModal() {
    const modal = document.createElement('div');
    modal.className = 'modal fade';
    modal.id = 'qrModal';
    modal.innerHTML = `
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Book QR Code</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body"></div>
            </div>
        </div>
    `;
    document.body.appendChild(modal);
    return modal;
}

function downloadQRCode(qrCodeData, bookTitle) {
    const link = document.createElement('a');
    link.download = `${bookTitle.replace(/[^a-z0-9]/gi, '_').toLowerCase()}_qr_code.png`;
    link.href = qrCodeData;
    link.click();
}

// Tooltips and UI Enhancements
function initializeTooltips() {
    // Initialize Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Copy to clipboard functionality
    const copyBtns = document.querySelectorAll('.copy-btn');
    copyBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const text = this.dataset.copyText;
            navigator.clipboard.writeText(text).then(() => {
                showNotification('Copied to clipboard!', 'success');
            }).catch(() => {
                showNotification('Failed to copy to clipboard.', 'error');
            });
        });
    });
}

// Autocomplete for search
function initializeAutocomplete() {
    const searchInput = document.getElementById('search-input');
    if (!searchInput) return;
    
    let autocompleteTimeout;
    let currentSuggestions = [];
    
    searchInput.addEventListener('input', function() {
        const query = this.value.trim();
        
        clearTimeout(autocompleteTimeout);
        
        if (query.length < 2) {
            hideAutocomplete();
            return;
        }
        
        autocompleteTimeout = setTimeout(() => {
            fetchAutocomplete(query);
        }, 300);
    });
    
    searchInput.addEventListener('blur', function() {
        setTimeout(hideAutocomplete, 150);
    });
    
    function fetchAutocomplete(query) {
        fetch(`/api/search/autocomplete?q=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                showAutocomplete(data.suggestions);
            })
            .catch(error => {
                console.error('Autocomplete error:', error);
            });
    }
    
    function showAutocomplete(suggestions) {
        let dropdown = document.getElementById('autocomplete-dropdown');
        
        if (!dropdown) {
            dropdown = document.createElement('div');
            dropdown.id = 'autocomplete-dropdown';
            dropdown.className = 'autocomplete-dropdown';
            searchInput.parentNode.appendChild(dropdown);
        }
        
        if (suggestions.length === 0) {
            hideAutocomplete();
            return;
        }
        
        dropdown.innerHTML = suggestions.map(suggestion => `
            <div class="autocomplete-item" onclick="selectSuggestion('${escapeHtml(suggestion.text)}')">
                <strong>${escapeHtml(suggestion.text)}</strong>
                <small class="text-muted">${suggestion.category || suggestion.type}</small>
            </div>
        `).join('');
        
        dropdown.style.display = 'block';
    }
    
    function hideAutocomplete() {
        const dropdown = document.getElementById('autocomplete-dropdown');
        if (dropdown) {
            dropdown.style.display = 'none';
        }
    }
    
    window.selectSuggestion = function(text) {
        searchInput.value = text;
        hideAutocomplete();
        updateSearchResults();
    };
}

// Price toggle for swap type
function initializePriceToggle() {
    const swapTypeSelect = document.getElementById('swap_type');
    const priceField = document.getElementById('price');
    const priceGroup = document.querySelector('#price').closest('.mb-3');
    
    if (swapTypeSelect && priceField) {
        function togglePriceField() {
            const showPrice = swapTypeSelect.value === 'sell';
            priceGroup.style.display = showPrice ? 'block' : 'none';
            priceField.required = showPrice;
            
            if (!showPrice) {
                priceField.value = '';
            }
        }
        
        swapTypeSelect.addEventListener('change', togglePriceField);
        togglePriceField(); // Initialize
    }
}

// Utility Functions
function showLoadingIndicator() {
    const indicator = document.getElementById('loading-indicator');
    if (indicator) {
        indicator.style.display = 'block';
    }
}

function hideLoadingIndicator() {
    const indicator = document.getElementById('loading-indicator');
    if (indicator) {
        indicator.style.display = 'none';
    }
}

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show notification-toast`;
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Add to page
    const container = document.querySelector('.container').firstElementChild || document.body;
    container.insertBefore(notification, container.firstChild);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, function(m) { return map[m]; });
}

function updatePagination(pagination) {
    const paginationContainer = document.getElementById('pagination-container');
    if (!paginationContainer || !pagination) return;
    
    let paginationHTML = '<nav><ul class="pagination justify-content-center">';
    
    // Previous button
    paginationHTML += `
        <li class="page-item ${pagination.has_prev ? '' : 'disabled'}">
            <a class="page-link" href="?page=${pagination.page - 1}" ${pagination.has_prev ? '' : 'tabindex="-1"'}>
                Previous
            </a>
        </li>
    `;
    
    // Page numbers
    const startPage = Math.max(1, pagination.page - 2);
    const endPage = Math.min(pagination.pages, pagination.page + 2);
    
    for (let i = startPage; i <= endPage; i++) {
        paginationHTML += `
            <li class="page-item ${i === pagination.page ? 'active' : ''}">
                <a class="page-link" href="?page=${i}">${i}</a>
            </li>
        `;
    }
    
    // Next button
    paginationHTML += `
        <li class="page-item ${pagination.has_next ? '' : 'disabled'}">
            <a class="page-link" href="?page=${pagination.page + 1}" ${pagination.has_next ? '' : 'tabindex="-1"'}>
                Next
            </a>
        </li>
    `;
    
    paginationHTML += '</ul></nav>';
    paginationContainer.innerHTML = paginationHTML;
}

// Enhanced book interaction
function addToWishlist(bookTitle, author = '', subject = '') {
    const formData = new FormData();
    formData.append('book_title', bookTitle);
    formData.append('author', author);
    formData.append('subject', subject);
    
    fetch('/add_to_wishlist', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            showNotification('Book added to wishlist!', 'success');
        } else {
            throw new Error('Failed to add to wishlist');
        }
    })
    .catch(error => {
        console.error('Error adding to wishlist:', error);
        showNotification('Failed to add to wishlist. Please try again.', 'error');
    });
}

// Initialize analytics charts (if Chart.js is available)
function initializeCharts() {
    if (typeof Chart === 'undefined') return;
    
    // Department distribution chart
    const deptChart = document.getElementById('departmentChart');
    if (deptChart) {
        new Chart(deptChart, {
            type: 'doughnut',
            data: {
                labels: window.chartData?.departments?.labels || [],
                datasets: [{
                    data: window.chartData?.departments?.data || [],
                    backgroundColor: [
                        '#FF6B35', '#138808', '#000080', '#FF9500', '#28A745', '#DC3545'
                    ]
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }
}

// Call chart initialization when document is ready
document.addEventListener('DOMContentLoaded', initializeCharts);

// Service Worker for offline capability (Progressive Web App)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        navigator.serviceWorker.register('/static/js/sw.js')
            .then(function(registration) {
                console.log('SW registered: ', registration);
            }, function(registrationError) {
                console.log('SW registration failed: ', registrationError);
            });
    });
}

// Export functions for global access
window.BookSwapBuddy = {
    showNotification,
    addToWishlist,
    showQRCode,
    updateSearchResults,
    escapeHtml
};
