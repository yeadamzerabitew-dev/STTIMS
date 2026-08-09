/**
 * STTIMS API Service
 * Handles all API calls to the backend
 */

const API_BASE = 'http://127.0.0.1:5000/api';

/**
 * Generic API call used by every *-api.js and page script
 * @param {string} endpoint - e.g. '/trainees' or '/trainees/5'
 * @param {string} method - GET | POST | PUT | DELETE
 * @param {object|null} data - request body for POST/PUT
 */
async function apiCall(endpoint, method = 'GET', data = null) {
    const options = {
        method,
        headers: {
            'Content-Type': 'application/json',
        },
        credentials: 'include',
    };

    if (data !== null) {
        options.body = JSON.stringify(data);
    }

    const response = await fetch(`${API_BASE}${endpoint}`, options);

    if (!response.ok) {
        let message = `HTTP error! status: ${response.status}`;
        try {
            const errBody = await response.json();
            message = errBody.message || errBody.error || message;
        } catch (_) {}
        throw new Error(message);
    }

    if (response.status === 204) {
        return null;
    }

    return await response.json();
}

console.log('🔌 api.js loaded successfully');
