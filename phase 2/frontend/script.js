// API Configuration
const API_BASE_URL = 'http://localhost:8000';

// DOM Elements
const loginForm = document.getElementById('loginForm');
const registerForm = document.getElementById('registerForm');
const loading = document.getElementById('loading');
const message = document.getElementById('message');

// Tab switching
function showTab(tabName) {
    // Hide all forms
    document.querySelectorAll('.auth-form').forEach(form => {
        form.classList.remove('active');
    });
    
    // Remove active class from all tabs
    document.querySelectorAll('.tab-button').forEach(button => {
        button.classList.remove('active');
    });
    
    // Show selected form
    document.getElementById(tabName + '-form').classList.add('active');
    
    // Add active class to clicked tab
    event.target.classList.add('active');
    
    // Clear messages
    hideMessage();
}

// Show loading spinner
function showLoading() {
    loading.classList.remove('hidden');
    loginForm.style.display = 'none';
    registerForm.style.display = 'none';
}

// Hide loading spinner
function hideLoading() {
    loading.classList.add('hidden');
    loginForm.style.display = 'block';
    registerForm.style.display = 'block';
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

// Store token in localStorage
function storeToken(token) {
    localStorage.setItem('access_token', token);
}

// Get token from localStorage
function getToken() {
    return localStorage.getItem('access_token');
}

// Clear token from localStorage
function clearToken() {
    localStorage.removeItem('access_token');
}

// Make API request
async function makeRequest(url, options = {}) {
    const token = getToken();
    
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
        const errorData = await response.json().catch(() => ({ detail: 'Network error' }));
        throw new Error(errorData.detail || `HTTP ${response.status}`);
    }
    
    return response.json();
}

// Login function
async function login(email, password) {
    try {
        const data = await makeRequest('/api/auth/login', {
            method: 'POST',
            body: JSON.stringify({ email, password })
        });
        
        storeToken(data.access_token);
        showMessage('Login successful! Redirecting...', 'success');
        
        // Redirect to dashboard after 2 seconds
        setTimeout(() => {
            window.location.href = 'dashboard.html';
        }, 2000);
        
    } catch (error) {
        showMessage(`Login failed: ${error.message}`, 'error');
    }
}

// Register function
async function register(userData) {
    try {
        const data = await makeRequest('/api/auth/register', {
            method: 'POST',
            body: JSON.stringify(userData)
        });
        
        showMessage('Registration successful! Please login.', 'success');
        
        // Switch to login tab after 2 seconds
        setTimeout(() => {
            showTab('login');
            // Pre-fill email
            document.getElementById('loginEmail').value = userData.email;
        }, 2000);
        
    } catch (error) {
        showMessage(`Registration failed: ${error.message}`, 'error');
    }
}

// Event Listeners
loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData(loginForm);
    const email = formData.get('email');
    const password = formData.get('password');
    
    if (!email || !password) {
        showMessage('Please fill in all fields', 'error');
        return;
    }
    
    showLoading();
    
    try {
        await login(email, password);
    } finally {
        hideLoading();
    }
});

registerForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData(registerForm);
    const userData = {
        full_name: formData.get('full_name'),
        email: formData.get('email'),
        password: formData.get('password'),
        role: formData.get('role')
    };
    
    if (!userData.full_name || !userData.email || !userData.password) {
        showMessage('Please fill in all required fields', 'error');
        return;
    }
    
    if (userData.password.length < 6) {
        showMessage('Password must be at least 6 characters long', 'error');
        return;
    }
    
    showLoading();
    
    try {
        await register(userData);
    } finally {
        hideLoading();
    }
});

// Check if user is already logged in
document.addEventListener('DOMContentLoaded', () => {
    const token = getToken();
    if (token) {
        // Verify token is still valid
        makeRequest('/api/auth/me')
            .then(() => {
                // Token is valid, redirect to dashboard
                window.location.href = 'dashboard.html';
            })
            .catch(() => {
                // Token is invalid, clear it
                clearToken();
            });
    }
});

// Form validation
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Add real-time validation
document.getElementById('registerEmail').addEventListener('blur', (e) => {
    const email = e.target.value;
    if (email && !validateEmail(email)) {
        showMessage('Please enter a valid email address', 'error');
    }
});

document.getElementById('registerPassword').addEventListener('input', (e) => {
    const password = e.target.value;
    if (password && password.length < 6) {
        showMessage('Password must be at least 6 characters long', 'error');
    }
});
