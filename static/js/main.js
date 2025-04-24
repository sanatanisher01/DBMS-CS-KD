// Main JavaScript for SportSphere

document.addEventListener('DOMContentLoaded', function() {
    // Add fade-in animation to main content
    const mainContent = document.querySelector('main');
    if (mainContent) {
        mainContent.classList.add('fade-in');
    }

    // Auto-dismiss alerts after 5 seconds
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Activate tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Activate popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Add active class to current nav item
    const currentLocation = window.location.pathname;
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href && currentLocation.includes(href) && href !== '/') {
            link.classList.add('active');
        } else if (href === '/' && currentLocation === '/') {
            link.classList.add('active');
        }
    });

    // Booking form validation and enhancement
    const bookingForm = document.getElementById('booking-form');
    if (bookingForm) {
        // Initialize date pickers with better UX
        const startTimeInput = document.getElementById('id_start_time');
        const endTimeInput = document.getElementById('id_end_time');

        if (startTimeInput && endTimeInput) {
            // Set minimum date to today
            const today = new Date();
            const todayStr = today.toISOString().slice(0, 16);
            startTimeInput.min = todayStr;

            // Update end time min when start time changes
            startTimeInput.addEventListener('change', function() {
                endTimeInput.min = this.value;
                if (endTimeInput.value && new Date(endTimeInput.value) <= new Date(this.value)) {
                    endTimeInput.value = '';
                }

                // Show visual feedback
                this.classList.add('is-valid');
            });

            endTimeInput.addEventListener('change', function() {
                if (this.value && startTimeInput.value) {
                    if (new Date(this.value) > new Date(startTimeInput.value)) {
                        this.classList.add('is-valid');
                        this.classList.remove('is-invalid');
                    } else {
                        this.classList.add('is-invalid');
                        this.classList.remove('is-valid');
                    }
                }
            });
        }

        // Form validation with better UX
        bookingForm.addEventListener('submit', function(event) {
            let isValid = true;
            const requiredFields = bookingForm.querySelectorAll('[required]');

            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    field.classList.add('is-invalid');
                    isValid = false;
                } else {
                    field.classList.remove('is-invalid');
                }
            });

            if (startTimeInput && endTimeInput && startTimeInput.value && endTimeInput.value) {
                const startDate = new Date(startTimeInput.value);
                const endDate = new Date(endTimeInput.value);

                if (endDate <= startDate) {
                    endTimeInput.classList.add('is-invalid');
                    isValid = false;

                    // Show error message
                    const errorDiv = document.createElement('div');
                    errorDiv.className = 'invalid-feedback';
                    errorDiv.textContent = 'End time must be after start time';

                    // Remove existing error message if any
                    const existingError = endTimeInput.nextElementSibling;
                    if (existingError && existingError.className === 'invalid-feedback') {
                        existingError.remove();
                    }

                    endTimeInput.parentNode.appendChild(errorDiv);
                }
            }

            if (!isValid) {
                event.preventDefault();
                // Scroll to first invalid field
                const firstInvalid = bookingForm.querySelector('.is-invalid');
                if (firstInvalid) {
                    firstInvalid.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    firstInvalid.focus();
                }
            }
        });
    }

    // Equipment filter with animation
    const facilitySelect = document.getElementById('facility-filter');
    if (facilitySelect) {
        facilitySelect.addEventListener('change', function() {
            const facilityId = this.value;
            const equipmentCards = document.querySelectorAll('.equipment-card');

            equipmentCards.forEach(function(card) {
                if (facilityId === '' || card.dataset.facilityId === facilityId) {
                    card.style.opacity = '0';
                    setTimeout(() => {
                        card.style.display = 'block';
                        setTimeout(() => {
                            card.style.opacity = '1';
                        }, 50);
                    }, 300);
                } else {
                    card.style.opacity = '0';
                    setTimeout(() => {
                        card.style.display = 'none';
                    }, 300);
                }
            });
        });
    }

    // Maintenance form facility/equipment selection with improved UX
    const maintenanceForm = document.getElementById('maintenance-form');
    if (maintenanceForm) {
        const facilitySelect = document.getElementById('id_facility');
        const equipmentSelect = document.getElementById('id_equipment');

        if (facilitySelect && equipmentSelect) {
            facilitySelect.addEventListener('change', function() {
                const facilityId = this.value;

                if (facilityId) {
                    // Show loading indicator
                    const loadingSpinner = document.createElement('div');
                    loadingSpinner.className = 'spinner-border spinner-border-sm text-primary ms-2';
                    loadingSpinner.setAttribute('role', 'status');
                    loadingSpinner.innerHTML = '<span class="visually-hidden">Loading...</span>';
                    facilitySelect.parentNode.appendChild(loadingSpinner);

                    // Fetch equipment for selected facility
                    fetch(`/api/facility/${facilityId}/equipment/`)
                        .then(response => response.json())
                        .then(data => {
                            // Clear current options
                            equipmentSelect.innerHTML = '<option value="">Select equipment (optional)</option>';

                            // Add new options
                            data.forEach(equipment => {
                                const option = document.createElement('option');
                                option.value = equipment.id;
                                option.textContent = equipment.name;
                                equipmentSelect.appendChild(option);
                            });

                            equipmentSelect.disabled = false;
                            equipmentSelect.classList.add('border-primary');

                            // Remove loading indicator
                            loadingSpinner.remove();
                        })
                        .catch(error => {
                            console.error('Error fetching equipment:', error);
                            // Remove loading indicator
                            loadingSpinner.remove();

                            // Show error message
                            const errorMsg = document.createElement('div');
                            errorMsg.className = 'text-danger mt-2';
                            errorMsg.textContent = 'Failed to load equipment. Please try again.';
                            facilitySelect.parentNode.appendChild(errorMsg);

                            // Remove error after 3 seconds
                            setTimeout(() => {
                                errorMsg.remove();
                            }, 3000);
                        });
                } else {
                    equipmentSelect.innerHTML = '<option value="">Select equipment (optional)</option>';
                    equipmentSelect.disabled = true;
                    equipmentSelect.classList.remove('border-primary');
                }
            });
        }
    }

    // Availability checker with improved UX
    const checkAvailabilityBtn = document.getElementById('check-availability-btn');
    if (checkAvailabilityBtn) {
        checkAvailabilityBtn.addEventListener('click', function() {
            const facilityId = document.getElementById('id_facility').value;
            const startTime = document.getElementById('id_start_time').value;
            const endTime = document.getElementById('id_end_time').value;
            const bookingId = document.getElementById('booking-id') ? document.getElementById('booking-id').value : '';
            const availabilityMessage = document.getElementById('availability-message');
            const submitBtn = document.getElementById('submit-booking-btn');

            if (!facilityId || !startTime || !endTime) {
                availabilityMessage.innerHTML = '<i class="bi bi-exclamation-triangle me-2"></i> Please fill in all fields';
                availabilityMessage.className = 'alert alert-warning';
                availabilityMessage.style.display = 'block';
                return;
            }

            // Show loading state
            checkAvailabilityBtn.disabled = true;
            checkAvailabilityBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Checking...';

            const formData = new FormData();
            formData.append('facility_id', facilityId);
            formData.append('start_time', startTime);
            formData.append('end_time', endTime);
            if (bookingId) {
                formData.append('booking_id', bookingId);
            }

            fetch('/api/check-availability/', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.available) {
                    availabilityMessage.innerHTML = '<i class="bi bi-check-circle me-2"></i> Time slot is available!';
                    availabilityMessage.className = 'alert alert-success';
                    submitBtn.disabled = false;
                    submitBtn.classList.add('btn-pulse');
                } else {
                    availabilityMessage.innerHTML = '<i class="bi bi-x-circle me-2"></i> Time slot is not available. Please select a different time.';
                    availabilityMessage.className = 'alert alert-danger';
                    submitBtn.disabled = true;
                    submitBtn.classList.remove('btn-pulse');
                }
                availabilityMessage.style.display = 'block';

                // Reset button state
                checkAvailabilityBtn.disabled = false;
                checkAvailabilityBtn.innerHTML = 'Check Availability';

                // Scroll to message
                availabilityMessage.scrollIntoView({ behavior: 'smooth', block: 'center' });
            })
            .catch(error => {
                console.error('Error:', error);
                availabilityMessage.innerHTML = '<i class="bi bi-exclamation-circle me-2"></i> An error occurred while checking availability';
                availabilityMessage.className = 'alert alert-danger';
                availabilityMessage.style.display = 'block';

                // Reset button state
                checkAvailabilityBtn.disabled = false;
                checkAvailabilityBtn.innerHTML = 'Check Availability';
            });
        });
    }

    // Add interactive charts to dashboard if Chart.js is available
    if (typeof Chart !== 'undefined') {
        // Facility usage chart
        const facilityUsageChart = document.getElementById('facilityUsageChart');
        if (facilityUsageChart) {
            new Chart(facilityUsageChart, {
                type: 'bar',
                data: {
                    labels: ['Basketball Court', 'Tennis Court', 'Swimming Pool', 'Gym', 'Football Field'],
                    datasets: [{
                        label: 'Bookings This Month',
                        data: [65, 42, 73, 89, 31],
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.7)',
                            'rgba(54, 162, 235, 0.7)',
                            'rgba(255, 206, 86, 0.7)',
                            'rgba(75, 192, 192, 0.7)',
                            'rgba(153, 102, 255, 0.7)'
                        ],
                        borderColor: [
                            'rgba(255, 99, 132, 1)',
                            'rgba(54, 162, 235, 1)',
                            'rgba(255, 206, 86, 1)',
                            'rgba(75, 192, 192, 1)',
                            'rgba(153, 102, 255, 1)'
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'top',
                        },
                        title: {
                            display: true,
                            text: 'Facility Usage Statistics'
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        }

        // Booking status chart
        const bookingStatusChart = document.getElementById('bookingStatusChart');
        if (bookingStatusChart) {
            new Chart(bookingStatusChart, {
                type: 'doughnut',
                data: {
                    labels: ['Approved', 'Pending', 'Rejected', 'Cancelled', 'Completed'],
                    datasets: [{
                        label: 'Booking Status',
                        data: [42, 15, 8, 12, 63],
                        backgroundColor: [
                            'rgba(40, 167, 69, 0.7)',
                            'rgba(255, 193, 7, 0.7)',
                            'rgba(220, 53, 69, 0.7)',
                            'rgba(108, 117, 125, 0.7)',
                            'rgba(23, 162, 184, 0.7)'
                        ],
                        borderColor: [
                            'rgba(40, 167, 69, 1)',
                            'rgba(255, 193, 7, 1)',
                            'rgba(220, 53, 69, 1)',
                            'rgba(108, 117, 125, 1)',
                            'rgba(23, 162, 184, 1)'
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'right',
                        },
                        title: {
                            display: true,
                            text: 'Booking Status Distribution'
                        }
                    }
                }
            });
        }

        // Weekly bookings chart
        const weeklyBookingsChart = document.getElementById('weeklyBookingsChart');
        if (weeklyBookingsChart) {
            new Chart(weeklyBookingsChart, {
                type: 'line',
                data: {
                    labels: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
                    datasets: [{
                        label: 'This Week',
                        data: [12, 19, 15, 17, 22, 30, 25],
                        borderColor: 'rgba(13, 110, 253, 1)',
                        backgroundColor: 'rgba(13, 110, 253, 0.1)',
                        tension: 0.3,
                        fill: true
                    }, {
                        label: 'Last Week',
                        data: [10, 15, 12, 14, 20, 27, 22],
                        borderColor: 'rgba(173, 181, 189, 1)',
                        borderDash: [5, 5],
                        tension: 0.3,
                        fill: false
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'top',
                        },
                        title: {
                            display: true,
                            text: 'Weekly Booking Trends'
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: 'Number of Bookings'
                            }
                        }
                    }
                }
            });
        }
    }

    // Add image preview for facility images
    const facilityImages = document.querySelectorAll('.facility-image');
    if (facilityImages.length > 0) {
        facilityImages.forEach(img => {
            img.addEventListener('click', function() {
                const modal = new bootstrap.Modal(document.getElementById('imagePreviewModal'));
                const modalImg = document.getElementById('previewImage');
                const modalTitle = document.getElementById('imagePreviewModalLabel');

                modalImg.src = this.src;
                modalTitle.textContent = this.alt;
                modal.show();
            });
        });
    }

    // Add smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId !== '#') {
                document.querySelector(targetId).scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
});

// Add pulse animation for buttons
.btn-pulse {
    animation: pulse 1.5s infinite;
}

@keyframes pulse {
    0% {
        box-shadow: 0 0 0 0 rgba(13, 110, 253, 0.7);
    }
    70% {
        box-shadow: 0 0 0 10px rgba(13, 110, 253, 0);
    }
    100% {
        box-shadow: 0 0 0 0 rgba(13, 110, 253, 0);
    }
}
