// API Configuration
const API_BASE_URL = 'http://localhost:8000';

// DOM Elements
const userName = document.getElementById('userName');
const userRole = document.getElementById('userRole');
const message = document.getElementById('message');

// Initialize dashboard
document.addEventListener('DOMContentLoaded', () => {
    checkAuthentication();
    loadUserInfo();
});

// Check if user is authenticated
function checkAuthentication() {
    const token = localStorage.getItem('access_token');
    if (!token) {
        window.location.href = 'index.html';
        return;
    }
}

// Load user information
async function loadUserInfo() {
    try {
        const userData = await makeRequest('/api/auth/me');
        userName.textContent = userData.full_name;
        userRole.textContent = userData.role.toUpperCase();
        userRole.className = `role-badge role-${userData.role}`;
    } catch (error) {
        showMessage('Failed to load user information', 'error');
        logout();
    }
}

// Make API request
async function makeRequest(url, options = {}) {
    const token = localStorage.getItem('access_token');
    
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
            ...(token && { 'Authorization': `Bearer ${token}` })
        }
    };
    
    const response = await fetch(`${API_BASE_URL}${url}`, {
        ...defaultOptions,
        ...options,
        headers: {
            ...defaultOptions.headers,
            ...options.headers
        }
    });
    
    if (!response.ok) {
        if (response.status === 401) {
            // Token expired, redirect to login
            localStorage.removeItem('access_token');
            window.location.href = 'index.html';
            return;
        }
        const errorData = await response.json().catch(() => ({ detail: 'Network error' }));
        throw new Error(errorData.detail || `HTTP ${response.status}`);
    }
    
    return response.json();
}

// Show message
function showMessage(text, type = 'info') {
    message.textContent = text;
    message.className = `message ${type}`;
    message.classList.remove('hidden');
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        hideMessage();
    }, 5000);
}

// Hide message
function hideMessage() {
    message.classList.add('hidden');
}

// Logout function
function logout() {
    localStorage.removeItem('access_token');
    window.location.href = 'index.html';
}

// Modal functions
function showModal(modalId) {
    document.getElementById(modalId).classList.remove('hidden');
}

function closeModal(modalId) {
    document.getElementById(modalId).classList.add('hidden');
}

// Show search form
function showSearchForm() {
    showModal('searchModal');
}

// Show team creation form
function showTeamForm() {
    showModal('teamModal');
}

// Show profile form (placeholder)
function showProfileForm() {
    showMessage('Company profile management coming soon!', 'info');
}

// Show saved tenders (placeholder)
function showSavedTenders() {
    showMessage('Saved tenders feature coming soon!', 'info');
}

// Search form submission
document.getElementById('searchForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const keywords = document.getElementById('searchKeywords').value;
    const province = document.getElementById('searchProvince').value;
    const budget = document.getElementById('searchBudget').value;
    
    if (!keywords.trim()) {
        showMessage('Please enter search keywords', 'error');
        return;
    }
    
    showMessage('Searching tenders...', 'info');
    
    try {
        // This would be the actual search API call
        // For now, we'll simulate it
        await new Promise(resolve => setTimeout(resolve, 2000));
        showMessage('Search completed! Results will be displayed here.', 'success');
        closeModal('searchModal');
    } catch (error) {
        showMessage(`Search failed: ${error.message}`, 'error');
    }
});

// Team creation form submission
document.getElementById('teamForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const teamData = {
        name: document.getElementById('teamName').value,
        description: document.getElementById('teamDescription').value,
        plan: document.getElementById('teamPlan').value
    };
    
    if (!teamData.name.trim()) {
        showMessage('Please enter a team name', 'error');
        return;
    }
    
    try {
        const result = await makeRequest('/api/teams/create', {
            method: 'POST',
            body: JSON.stringify(teamData)
        });
        
        showMessage(`Team "${result.name}" created successfully!`, 'success');
        closeModal('teamModal');
        
        // Reset form
        document.getElementById('teamForm').reset();
        
    } catch (error) {
        showMessage(`Failed to create team: ${error.message}`, 'error');
    }
});

// Close modals when clicking outside
document.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal')) {
        e.target.classList.add('hidden');
    }
});

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        // Close any open modals
        document.querySelectorAll('.modal').forEach(modal => {
            modal.classList.add('hidden');
        });
    }
});
