
// Configuration
const API_BASE_URL = 'http://127.0.0.1:5000';
const BACKEND_CHECK_INTERVAL = 5000; // Check every 5 seconds

// Global variables
let backendAvailable = false;
let requiredFeatures = [];

// ===== INITIALIZATION =====
document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ Page loaded');
    
    // Check backend availability
    checkBackendConnection();
    
    // Set up periodic backend check
    setInterval(checkBackendConnection, BACKEND_CHECK_INTERVAL);
});

// ===== BACKEND CONNECTION =====
/**
 * Check if backend is running and accessible
 */
async function checkBackendConnection() {
    try {
        const response = await fetch(`${API_BASE_URL}/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        if (response.ok) {
            backendAvailable = true;
            updateStatusMessage('✅ Backend connected and ready', false);
            
            // Load features if not already loaded
            if (requiredFeatures.length === 0) {
                loadFeatures();
            }
        } else {
            backendAvailable = false;
            updateStatusMessage('⚠️  Backend error', true);
        }
    } catch (error) {
        backendAvailable = false;
        updateStatusMessage('❌ Backend not running. Please start: python backend/app.py', true);
        console.error('Backend connection error:', error);
    }
}

/**
 * Load required features from backend
 */
async function loadFeatures() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/features`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        if (response.ok) {
            const data = await response.json();
            requiredFeatures = data.features;
            console.log('✅ Features loaded:', requiredFeatures);
        }
    } catch (error) {
        console.error('Error loading features:', error);
    }
}

/**
 * Update status message
 */
function updateStatusMessage(message, isError = false) {
    const statusEl = document.getElementById('statusMessage');
    if (statusEl) {
        statusEl.textContent = message;
        statusEl.className = isError ? 'status-error' : '';
    }
}

// ===== FORM OPERATIONS =====

/**
 * Collect form data
 */
function getFormData() {
    const data = {
        age: parseFloat(document.getElementById('age').value) || 0,
        income: parseFloat(document.getElementById('income').value) || 0,
        credit_limit: parseFloat(document.getElementById('credit_limit').value) || 0,
        debt_ratio: parseFloat(document.getElementById('debt_ratio').value) || 0,
        monthly_debt: parseFloat(document.getElementById('monthly_debt').value) || 0,
        number_of_open_accounts: parseFloat(document.getElementById('number_of_open_accounts').value) || 0,
        number_of_times_90_days_late: parseFloat(document.getElementById('number_of_times_90_days_late').value) || 0,
        age_of_credit_line: parseFloat(document.getElementById('age_of_credit_line').value) || 0,
        number_of_times_60_days_late: parseFloat(document.getElementById('number_of_times_60_days_late').value) || 0,
        number_of_dependents: parseFloat(document.getElementById('number_of_dependents').value) || 0
    };
    
    return data;
}

/**
 * Validate form data
 */
function validateFormData(data) {
    const errors = [];
    
    if (data.age < 18 || data.age > 100) {
        errors.push('Age must be between 18 and 100');
    }
    
    if (data.income < 0) {
        errors.push('Income cannot be negative');
    }
    
    if (data.debt_ratio < 0) {
        errors.push('Debt-to-income ratio cannot be negative');
    }
    
    return errors;
}

/**
 * Predict credit risk
 */
async function predictRisk() {
    // Check backend
    if (!backendAvailable) {
        alert('❌ Backend is not running. Please start: python backend/app.py');
        return;
    }
    
    // Get form data
    const formData = getFormData();
    
    // Validate
    const errors = validateFormData(formData);
    if (errors.length > 0) {
        alert('⚠️  Please fix these errors:\n\n' + errors.join('\n'));
        return;
    }
    
    // Show loading
    document.getElementById('loading').style.display = 'flex';
    document.getElementById('results').style.display = 'none';
    
    try {
        // Make API call
        const response = await fetch(`${API_BASE_URL}/api/predict`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (response.ok && data.status === 'success') {
            displayResults(data);
        } else {
            alert('❌ Prediction error: ' + (data.message || 'Unknown error'));
        }
    } catch (error) {
        console.error('Prediction error:', error);
        alert('❌ Error connecting to backend:\n' + error.message);
    } finally {
        document.getElementById('loading').style.display = 'none';
    }
}

/**
 * Display prediction results
 */
function displayResults(data) {
    // Show results container
    document.getElementById('results').style.display = 'block';
    
    // Update risk score
    const riskScore = parseFloat(data.risk_score);
    document.getElementById('riskScore').textContent = riskScore.toFixed(3);
    
    // Update risk level and recommendation
    document.getElementById('riskLevel').textContent = data.risk_level;
    document.getElementById('recommendation').textContent = data.recommendation;
    document.getElementById('timestamp').textContent = new Date(data.timestamp).toLocaleString();
    
    // Update risk indicator position
    const riskIndicator = document.getElementById('riskIndicator');
    riskIndicator.innerHTML = ''; // Clear previous pointer
    
    const pointerPosition = riskScore * 100; // Convert 0-1 to 0-100
    const pointer = document.createElement('div');
    pointer.className = 'risk-indicator-pointer';
    pointer.style.left = pointerPosition + '%';
    riskIndicator.appendChild(pointer);
    
    // Update result card color based on risk level
    const resultCard = document.getElementById('resultCard');
    resultCard.style.borderLeftColor = data.color;
    
    // Color mapping
    const colorMap = {
        'green': '#27ae60',
        'orange': '#f39c12',
        'red': '#e74c3c'
    };
    
    document.getElementById('riskScore').style.color = colorMap[data.color] || '#3498db';
    
    // Log results
    console.log('✅ Prediction results:', data);
}

/**
 * Clear the form
 */
function clearForm() {
    document.getElementById('age').value = '';
    document.getElementById('income').value = '';
    document.getElementById('credit_limit').value = '';
    document.getElementById('debt_ratio').value = '';
    document.getElementById('monthly_debt').value = '';
    document.getElementById('number_of_open_accounts').value = '';
    document.getElementById('number_of_times_90_days_late').value = '';
    document.getElementById('age_of_credit_line').value = '';
    document.getElementById('number_of_times_60_days_late').value = '';
    document.getElementById('number_of_dependents').value = '';
    
    document.getElementById('results').style.display = 'none';
    document.getElementById('loading').style.display = 'none';
    
    console.log('🔄 Form cleared');
}

// ===== UTILITY FUNCTIONS =====

/**
 * Format number as currency
 */
function formatCurrency(value) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(value);
}

/**
 * Format percentage
 */
function formatPercentage(value) {
    return (value * 100).toFixed(2) + '%';
}

/**
 * Log message with timestamp
 */
function log(message) {
    const timestamp = new Date().toLocaleTimeString();
    console.log(`[${timestamp}] ${message}`);
}

// ===== ERROR HANDLING =====

/**
 * Global error handler
 */
window.addEventListener('error', function(event) {
    console.error('❌ Error:', event.error);
});

/**
 * Handle unhandled promise rejections
 */
window.addEventListener('unhandledrejection', function(event) {
    console.error('❌ Unhandled rejection:', event.reason);
});

// ===== API TEST FUNCTION =====

/**
 * Test the API (for debugging)
 */
async function testAPI() {
    console.log('🧪 Testing API endpoints...');
    
    try {
        // Test home endpoint
        console.log('\n📍 Testing GET /');
        const homeResponse = await fetch(`${API_BASE_URL}/`, {
            method: 'GET'
        });
        console.log('Response:', await homeResponse.json());
        
        // Test features endpoint
        console.log('\n📍 Testing GET /api/features');
        const featuresResponse = await fetch(`${API_BASE_URL}/api/features`, {
            method: 'GET'
        });
        console.log('Response:', await featuresResponse.json());
        
        // Test model info endpoint
        console.log('\n📍 Testing GET /api/model-info');
        const infoResponse = await fetch(`${API_BASE_URL}/api/model-info`, {
            method: 'GET'
        });
        console.log('Response:', await infoResponse.json());
        
        console.log('\n✅ All tests passed!');
    } catch (error) {
        console.error('❌ Test failed:', error);
    }
}

// ===== DEBUG MODE =====

/**
 * Enable debug logging
 */
function enableDebug() {
    window.DEBUG_MODE = true;
    console.log('🐛 Debug mode enabled');
    console.log('Available commands:');
    console.log('  - testAPI()');
    console.log('  - checkBackendConnection()');
    console.log('  - getFormData()');
    console.log('  - clearForm()');
}

/**
 * Log app state (for debugging)
 */
function logAppState() {
    console.log('=== APP STATE ===');
    console.log('Backend Available:', backendAvailable);
    console.log('Required Features:', requiredFeatures);
    console.log('Form Data:', getFormData());
    console.log('================');
}
