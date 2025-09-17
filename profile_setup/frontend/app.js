/**
 * SED Tender Insight Hub - Frontend Application
 * Profile Setup & Scoring Interface
 */

class ProfileManager {
    constructor() {
        this.apiBaseUrl = 'http://localhost:5000/api';
        this.token = localStorage.getItem('authToken');
        this.currentProfile = null;
        this.init();
    }

    async init() {
        // Check authentication
        if (!this.token) {
            this.showLoginModal();
            return;
        }

        // Load user profile
        await this.loadProfile();
        
        // Setup event listeners
        this.setupEventListeners();
        
        // Update UI
        this.updateUI();
    }

    setupEventListeners() {
        // Form submissions
        document.getElementById('cidbForm').addEventListener('submit', (e) => this.handleFormSubmit(e, 'cidb'));
        document.getElementById('beeForm').addEventListener('submit', (e) => this.handleFormSubmit(e, 'bee'));
        document.getElementById('companyForm').addEventListener('submit', (e) => this.handleFormSubmit(e, 'company'));
        document.getElementById('experienceForm').addEventListener('submit', (e) => this.handleFormSubmit(e, 'experience'));

        // Real-time success rate calculation
        document.getElementById('previousTenderWins').addEventListener('input', () => this.calculateSuccessRate());
        document.getElementById('previousTenderApplications').addEventListener('input', () => this.calculateSuccessRate());

        // Tab change events
        document.querySelectorAll('[data-bs-toggle="pill"]').forEach(tab => {
            tab.addEventListener('shown.bs.tab', (e) => this.onTabChange(e));
        });
    }

    async loadProfile() {
        try {
            this.showLoading(true);
            const response = await this.apiCall('/profiles', 'GET');
            
            if (response.profile) {
                this.currentProfile = response.profile;
                this.populateForms();
            }
        } catch (error) {
            console.error('Error loading profile:', error);
            this.showAlert('Error loading profile: ' + error.message, 'error');
        } finally {
            this.showLoading(false);
        }
    }

    populateForms() {
        if (!this.currentProfile) return;

        // CIDB Information
        if (this.currentProfile.cidb_grade) {
            document.getElementById('cidbGrade').value = this.currentProfile.cidb_grade;
        }
        if (this.currentProfile.cidb_registration_number) {
            document.getElementById('cidbRegNumber').value = this.currentProfile.cidb_registration_number;
        }
        if (this.currentProfile.cidb_expiry_date) {
            document.getElementById('cidbExpiryDate').value = this.currentProfile.cidb_expiry_date;
        }
        if (this.currentProfile.cidb_work_categories) {
            const categories = Array.isArray(this.currentProfile.cidb_work_categories) 
                ? this.currentProfile.cidb_work_categories 
                : [];
            Array.from(document.getElementById('cidbWorkCategories').options).forEach(option => {
                option.selected = categories.includes(option.value);
            });
        }

        // BEE Information
        if (this.currentProfile.bee_level) {
            document.getElementById('beeLevel').value = this.currentProfile.bee_level;
        }
        if (this.currentProfile.bee_certificate_number) {
            document.getElementById('beeCertNumber').value = this.currentProfile.bee_certificate_number;
        }
        if (this.currentProfile.bee_expiry_date) {
            document.getElementById('beeExpiryDate').value = this.currentProfile.bee_expiry_date;
        }
        if (this.currentProfile.bee_ownership_percentage) {
            document.getElementById('beeOwnership').value = this.currentProfile.bee_ownership_percentage;
        }
        if (this.currentProfile.bee_management_control_percentage) {
            document.getElementById('beeManagement').value = this.currentProfile.bee_management_control_percentage;
        }
        if (this.currentProfile.bee_skills_development_percentage) {
            document.getElementById('beeSkills').value = this.currentProfile.bee_skills_development_percentage;
        }
        if (this.currentProfile.bee_enterprise_development_percentage) {
            document.getElementById('beeEnterprise').value = this.currentProfile.bee_enterprise_development_percentage;
        }
        if (this.currentProfile.bee_socio_economic_development_percentage) {
            document.getElementById('beeSocio').value = this.currentProfile.bee_socio_economic_development_percentage;
        }

        // Company Information
        if (this.currentProfile.years_in_business) {
            document.getElementById('yearsInBusiness').value = this.currentProfile.years_in_business;
        }
        if (this.currentProfile.annual_turnover) {
            document.getElementById('annualTurnover').value = this.currentProfile.annual_turnover;
        }
        if (this.currentProfile.number_of_employees) {
            document.getElementById('numberOfEmployees').value = this.currentProfile.number_of_employees;
        }

        // Experience Information
        if (this.currentProfile.previous_tender_wins) {
            document.getElementById('previousTenderWins').value = this.currentProfile.previous_tender_wins;
        }
        if (this.currentProfile.previous_tender_applications) {
            document.getElementById('previousTenderApplications').value = this.currentProfile.previous_tender_applications;
        }

        // Calculate success rate
        this.calculateSuccessRate();
    }

    async handleFormSubmit(event, formType) {
        event.preventDefault();
        
        try {
            this.showLoading(true);
            
            const formData = new FormData(event.target);
            const data = {};
            
            // Convert form data to object
            for (let [key, value] of formData.entries()) {
                if (key === 'cidb_work_categories') {
                    // Handle multiple select
                    if (!data[key]) data[key] = [];
                    data[key].push(value);
                } else if (value !== '') {
                    data[key] = value;
                }
            }

            // Special handling for CIDB work categories
            if (formType === 'cidb') {
                const selectedCategories = Array.from(document.getElementById('cidbWorkCategories').selectedOptions)
                    .map(option => option.value);
                data.cidb_work_categories = selectedCategories;
            }

            // Convert numeric fields
            const numericFields = [
                'cidb_grade', 'bee_level', 'years_in_business', 'annual_turnover',
                'number_of_employees', 'previous_tender_wins', 'previous_tender_applications',
                'bee_ownership_percentage', 'bee_management_control_percentage',
                'bee_skills_development_percentage', 'bee_enterprise_development_percentage',
                'bee_socio_economic_development_percentage'
            ];
            
            numericFields.forEach(field => {
                if (data[field] !== undefined) {
                    data[field] = parseFloat(data[field]) || 0;
                }
            });

            const response = await this.apiCall('/profiles', 'PUT', data);
            
            // Update current profile with new data
            this.currentProfile = { ...this.currentProfile, ...data };
            
            // Update scores
            if (response.profile) {
                this.currentProfile.readiness_score = response.profile.readiness_score;
                this.currentProfile.profile_completion_percentage = response.profile.profile_completion_percentage;
                this.currentProfile.last_score_calculation = response.profile.last_score_calculation;
            }
            
            this.updateUI();
            this.showAlert(`${formType.toUpperCase()} information saved successfully!`, 'success');
            
        } catch (error) {
            console.error('Error saving profile:', error);
            this.showAlert('Error saving profile: ' + error.message, 'error');
        } finally {
            this.showLoading(false);
        }
    }

    calculateSuccessRate() {
        const wins = parseInt(document.getElementById('previousTenderWins').value) || 0;
        const applications = parseInt(document.getElementById('previousTenderApplications').value) || 0;
        
        let successRate = 0;
        if (applications > 0) {
            successRate = Math.round((wins / applications) * 100);
        }
        
        document.getElementById('successRate').textContent = `${successRate}%`;
    }

    updateUI() {
        if (!this.currentProfile) return;

        // Update profile overview
        document.getElementById('companyName').textContent = this.currentProfile.company_name || '-';
        document.getElementById('companyReg').textContent = this.currentProfile.company_registration_number || '-';
        document.getElementById('phoneNumber').textContent = this.currentProfile.phone_number || '-';
        
        // Update completion badge
        const completion = this.currentProfile.profile_completion_percentage || 0;
        document.getElementById('completionBadge').textContent = `${completion}%`;
        
        // Update last updated
        if (this.currentProfile.updated_at) {
            const date = new Date(this.currentProfile.updated_at);
            document.getElementById('lastUpdated').textContent = date.toLocaleDateString();
        }

        // Update readiness score
        const score = this.currentProfile.readiness_score || 0;
        document.getElementById('scoreValue').textContent = score;
        
        // Update circular progress
        const circle = document.getElementById('scoreCircle');
        const circumference = 2 * Math.PI * 50; // radius = 50
        const offset = circumference - (score / 100) * circumference;
        circle.style.strokeDashoffset = offset;
        
        // Update score description
        let description = 'Complete your profile to improve your score';
        if (score >= 80) {
            description = 'Excellent! You have a high readiness score';
        } else if (score >= 60) {
            description = 'Good! Your readiness score is above average';
        } else if (score >= 40) {
            description = 'Fair. Consider completing more profile sections';
        } else if (score > 0) {
            description = 'Low score. Please complete your profile';
        }
        document.getElementById('scoreDescription').textContent = description;
    }

    async recalculateScore() {
        try {
            this.showLoading(true);
            const response = await this.apiCall('/profiles/score', 'POST');
            
            // Update current profile with new scores
            this.currentProfile.readiness_score = response.readiness_score;
            this.currentProfile.profile_completion_percentage = response.profile_completion_percentage;
            this.currentProfile.last_score_calculation = response.last_score_calculation;
            
            this.updateUI();
            this.showAlert('Score recalculated successfully!', 'success');
            
        } catch (error) {
            console.error('Error recalculating score:', error);
            this.showAlert('Error recalculating score: ' + error.message, 'error');
        } finally {
            this.showLoading(false);
        }
    }

    exportProfile() {
        if (!this.currentProfile) {
            this.showAlert('No profile data to export', 'error');
            return;
        }

        const dataStr = JSON.stringify(this.currentProfile, null, 2);
        const dataBlob = new Blob([dataStr], { type: 'application/json' });
        
        const link = document.createElement('a');
        link.href = URL.createObjectURL(dataBlob);
        link.download = `profile-export-${new Date().toISOString().split('T')[0]}.json`;
        link.click();
        
        this.showAlert('Profile exported successfully!', 'success');
    }

    onTabChange(event) {
        // Add any tab-specific logic here
        console.log('Tab changed to:', event.target.getAttribute('data-bs-target'));
    }

    async apiCall(endpoint, method = 'GET', data = null) {
        const url = `${this.apiBaseUrl}${endpoint}`;
        const options = {
            method,
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.token}`
            }
        };

        if (data && method !== 'GET') {
            options.body = JSON.stringify(data);
        }

        const response = await fetch(url, options);
        
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({ error: 'Unknown error' }));
            throw new Error(errorData.error || `HTTP ${response.status}`);
        }

        return await response.json();
    }

    showLoading(show) {
        const modal = new bootstrap.Modal(document.getElementById('loadingModal'));
        if (show) {
            modal.show();
        } else {
            modal.hide();
        }
    }

    showAlert(message, type = 'success') {
        const toast = document.getElementById('alertToast');
        const toastMessage = document.getElementById('toastMessage');
        const toastHeader = toast.querySelector('.toast-header');
        const icon = toastHeader.querySelector('i');
        
        toastMessage.textContent = message;
        
        if (type === 'error') {
            icon.className = 'fas fa-exclamation-circle text-danger me-2';
            toastHeader.querySelector('strong').textContent = 'Error';
        } else {
            icon.className = 'fas fa-check-circle text-success me-2';
            toastHeader.querySelector('strong').textContent = 'Success';
        }
        
        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();
    }

    showLoginModal() {
        // Simple login modal - in a real app, this would be more sophisticated
        const email = prompt('Please enter your email:');
        const password = prompt('Please enter your password:');
        
        if (email && password) {
            this.login(email, password);
        } else {
            alert('Login required to access the profile system');
        }
    }

    async login(email, password) {
        try {
            const response = await fetch(`${this.apiBaseUrl}/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email, password })
            });

            if (response.ok) {
                const data = await response.json();
                this.token = data.token;
                localStorage.setItem('authToken', this.token);
                await this.loadProfile();
                this.updateUI();
            } else {
                const errorData = await response.json();
                alert('Login failed: ' + errorData.error);
            }
        } catch (error) {
            console.error('Login error:', error);
            alert('Login failed: ' + error.message);
        }
    }

    logout() {
        this.token = null;
        localStorage.removeItem('authToken');
        this.currentProfile = null;
        location.reload();
    }
}

// Global functions for button clicks
function recalculateScore() {
    if (window.profileManager) {
        window.profileManager.recalculateScore();
    }
}

function exportProfile() {
    if (window.profileManager) {
        window.profileManager.exportProfile();
    }
}

function logout() {
    if (window.profileManager) {
        window.profileManager.logout();
    }
}

// Initialize the application when the page loads
document.addEventListener('DOMContentLoaded', () => {
    window.profileManager = new ProfileManager();
});

// Add some utility functions for form validation
function validateForm(formId) {
    const form = document.getElementById(formId);
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}

// Add real-time validation
document.addEventListener('input', (e) => {
    if (e.target.hasAttribute('required')) {
        if (e.target.value.trim()) {
            e.target.classList.remove('is-invalid');
        } else {
            e.target.classList.add('is-invalid');
        }
    }
});

// Add number formatting for currency fields
document.getElementById('annualTurnover').addEventListener('blur', (e) => {
    const value = parseFloat(e.target.value);
    if (!isNaN(value)) {
        e.target.value = value.toLocaleString('en-ZA');
    }
});

// Add percentage validation for BEE fields
document.querySelectorAll('input[name*="percentage"]').forEach(input => {
    input.addEventListener('blur', (e) => {
        const value = parseFloat(e.target.value);
        if (!isNaN(value) && (value < 0 || value > 100)) {
            e.target.classList.add('is-invalid');
            e.target.setCustomValidity('Percentage must be between 0 and 100');
        } else {
            e.target.classList.remove('is-invalid');
            e.target.setCustomValidity('');
        }
    });
});

