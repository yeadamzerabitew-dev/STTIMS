/* ============================================
   STTIMS - Authentication Module
   ============================================ */

class Auth {
    constructor() {
        this.apiBase = 'http://localhost:5000/api';
        this.token = null;
        this.user = null;
        this.init();
    }

    init() {
        // Check for existing session
        this.checkSession();
        
        // Setup login form
        this.setupLoginForm();
        
        // Setup logout buttons
        this.setupLogout();
    }

    // ============================================
    // Session Management
    // ============================================
    
    checkSession() {
        const user = localStorage.getItem('user') || sessionStorage.getItem('user');
        if (user) {
            try {
                this.user = JSON.parse(user);
                return true;
            } catch (e) {
                this.clearSession();
                return false;
            }
        }
        return false;
    }

    setSession(user, remember = false) {
        this.user = user;
        if (remember) {
            localStorage.setItem('user', JSON.stringify(user));
        } else {
            sessionStorage.setItem('user', JSON.stringify(user));
        }
    }

    clearSession() {
        this.user = null;
        localStorage.removeItem('user');
        sessionStorage.removeItem('user');
    }

    getUser() {
        return this.user;
    }

    isAuthenticated() {
        return this.user !== null && this.user !== undefined;
    }

    // ============================================
    // Login
    // ============================================
    
    async login(usernameOrEmail, password, remember = false) {
        try {
            const response = await fetch(`${this.apiBase}/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username_or_email: usernameOrEmail,
                    password: password
                })
            });

            const data = await response.json();

            if (!response.ok) {
                return {
                    success: false,
                    error: data.error || 'Login failed',
                    remaining_attempts: data.remaining_attempts
                };
            }

            // Login successful
            this.setSession(data.user, remember);
            
            return {
                success: true,
                user: data.user
            };

        } catch (error) {
            console.error('Login error:', error);
            return {
                success: false,
                error: 'Network error. Please try again.'
            };
        }
    }

    // ============================================
    // Logout
    // ============================================
    
    async logout() {
        try {
            await fetch(`${this.apiBase}/auth/logout`, {
                method: 'POST',
                credentials: 'include'
            });
        } catch (error) {
            console.warn('Logout API error:', error);
        } finally {
            this.clearSession();
            window.location.href = 'login.html';
        }
    }

    // ============================================
    // UI Setup
    // ============================================
    
    setupLoginForm() {
        const form = document.getElementById('loginForm');
        if (!form) return;

        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const username = document.getElementById('usernameOrEmail')?.value;
            const password = document.getElementById('password')?.value;
            const remember = document.getElementById('rememberMe')?.checked || false;
            const loginBtn = document.getElementById('loginBtn');
            const loginBtnText = document.getElementById('loginBtnText');
            const loginBtnSpinner = document.getElementById('loginBtnSpinner');

            // Validate
            if (!username || !password) {
                this.showAlert('Please fill in all fields', 'warning');
                return;
            }

            // Show loading
            loginBtn.disabled = true;
            loginBtnText.style.display = 'none';
            loginBtnSpinner.style.display = 'inline-block';

            const result = await this.login(username, password, remember);

            // Hide loading
            loginBtn.disabled = false;
            loginBtnText.style.display = 'inline-block';
            loginBtnSpinner.style.display = 'none';

            if (result.success) {
                this.showAlert('Login successful! Redirecting...', 'success');
                setTimeout(() => {
                    window.location.href = 'dashboard.html';
                }, 1000);
            } else {
                if (result.remaining_attempts !== undefined) {
                    this.showAlert(`Invalid credentials. ${result.remaining_attempts} attempts remaining.`, 'warning');
                } else {
                    this.showAlert(result.error || 'Login failed. Please try again.', 'danger');
                }
                document.getElementById('password').value = '';
                document.getElementById('password').focus();
            }
        });
    }

    setupLogout() {
        const logoutBtns = document.querySelectorAll('.logout-btn');
        logoutBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                if (confirm('Are you sure you want to logout?')) {
                    this.logout();
                }
            });
        });
    }

    // ============================================
    // Alert System
    // ============================================
    
    showAlert(message, type = 'info') {
        const container = document.getElementById('alertContainer');
        if (!container) return;

        const icons = {
            success: 'fa-check-circle',
            danger: 'fa-exclamation-circle',
            warning: 'fa-exclamation-triangle',
            info: 'fa-info-circle'
        };

        container.innerHTML = `
            <div class="alert alert-${type} alert-dismissible fade show" role="alert">
                <i class="fas ${icons[type] || icons.info} me-2"></i>
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;

        setTimeout(() => {
            const alert = container.querySelector('.alert');
            if (alert) {
                alert.classList.remove('show');
                setTimeout(() => container.innerHTML = '', 300);
            }
        }, 5000);
    }
}

// Initialize auth when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.auth = new Auth();
});

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = Auth;
}
