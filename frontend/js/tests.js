/* ============================================
   STTIMS - Automated Tests
   ============================================ */

/**
 * Test Runner
 */
class TestRunner {
    constructor() {
        this.tests = [];
        this.results = {
            passed: 0,
            failed: 0,
            total: 0
        };
    }

    /**
     * Add a test
     */
    addTest(name, fn) {
        this.tests.push({ name, fn });
    }

    /**
     * Run all tests
     */
    async run() {
        console.log('========================================');
        console.log('🧪 Running STTIMS Tests');
        console.log('========================================\n');

        for (const test of this.tests) {
            try {
                await test.fn();
                this.results.passed++;
                console.log(`✅ PASSED: ${test.name}`);
            } catch (error) {
                this.results.failed++;
                console.log(`❌ FAILED: ${test.name}`);
                console.log(`   Error: ${error.message}`);
            }
            this.results.total++;
        }

        this.printSummary();
    }

    /**
     * Print test summary
     */
    printSummary() {
        console.log('\n========================================');
        console.log('📊 Test Summary');
        console.log('========================================');
        console.log(`Total: ${this.results.total}`);
        console.log(`✅ Passed: ${this.results.passed}`);
        console.log(`❌ Failed: ${this.results.failed}`);
        console.log(`📈 Rate: ${(this.results.passed / this.results.total * 100).toFixed(2)}%`);
        console.log('========================================');
    }
}

/**
 * Assertion Helper
 */
function assert(condition, message) {
    if (!condition) {
        throw new Error(message || 'Assertion failed');
    }
}

function assertEqual(actual, expected, message) {
    if (actual !== expected) {
        throw new Error(message || `Expected ${expected}, got ${actual}`);
    }
}

function assertContains(array, item, message) {
    if (!array.includes(item)) {
        throw new Error(message || `Array does not contain ${item}`);
    }
}

// ============================================
// Navigation Tests
// ============================================
function navigationTests(runner) {
    runner.addTest('Sidebar navigation links exist', () => {
        const links = document.querySelectorAll('.sidebar .nav-link');
        assert(links.length > 0, 'No sidebar links found');
    });

    runner.addTest('Active link is highlighted', () => {
        const active = document.querySelector('.sidebar .nav-link.active');
        assert(active !== null, 'No active link found');
    });
}

// ============================================
// Login Tests
// ============================================
function loginTests(runner) {
    runner.addTest('Login form exists', () => {
        const form = document.getElementById('loginForm');
        assert(form !== null, 'Login form not found');
    });

    runner.addTest('Username field exists', () => {
        const field = document.getElementById('usernameOrEmail');
        assert(field !== null, 'Username field not found');
    });

    runner.addTest('Password field exists', () => {
        const field = document.getElementById('password');
        assert(field !== null, 'Password field not found');
    });

    runner.addTest('Login button exists', () => {
        const btn = document.getElementById('loginBtn');
        assert(btn !== null, 'Login button not found');
    });
}

// ============================================
// Dashboard Tests
// ============================================
function dashboardTests(runner) {
    runner.addTest('Dashboard statistics cards exist', () => {
        const cards = document.querySelectorAll('.stat-card');
        assert(cards.length >= 4, 'Not enough stat cards');
    });

    runner.addTest('Welcome banner exists', () => {
        const banner = document.querySelector('.welcome-banner');
        assert(banner !== null, 'Welcome banner not found');
    });

    runner.addTest('Chart canvas exists', () => {
        const chart = document.getElementById('enrollmentChart');
        assert(chart !== null, 'Chart not found');
    });
}

// ============================================
// Table Tests
// ============================================
function tableTests(runner, tableId) {
    runner.addTest(`${tableId} table exists`, () => {
        const table = document.getElementById(tableId);
        assert(table !== null, `Table ${tableId} not found`);
    });

    runner.addTest(`${tableId} has headers`, () => {
        const headers = document.querySelectorAll(`#${tableId} thead th`);
        assert(headers.length > 0, 'No table headers found');
    });

    runner.addTest(`${tableId} has tbody`, () => {
        const tbody = document.querySelector(`#${tableId} tbody`);
        assert(tbody !== null, 'Table body not found');
    });
}

// ============================================
// Form Tests
// ============================================
function formTests(runner, formId, fields) {
    runner.addTest(`${formId} form exists`, () => {
        const form = document.getElementById(formId);
        assert(form !== null, `Form ${formId} not found`);
    });

    fields.forEach(field => {
        runner.addTest(`${formId} has field ${field}`, () => {
            const element = document.getElementById(field);
            assert(element !== null, `Field ${field} not found`);
        });
    });

    runner.addTest(`${formId} has submit button`, () => {
        const btn = document.querySelector(`#${formId} button[type="submit"]`);
        assert(btn !== null, 'Submit button not found');
    });
}

// ============================================
// Modal Tests
// ============================================
function modalTests(runner, modalId) {
    runner.addTest(`${modalId} modal exists`, () => {
        const modal = document.getElementById(modalId);
        assert(modal !== null, `Modal ${modalId} not found`);
    });

    runner.addTest(`${modalId} has close button`, () => {
        const btn = document.querySelector(`#${modalId} .btn-close`);
        assert(btn !== null, 'Close button not found');
    });
}

// ============================================
// Validation Tests
// ============================================
function validationTests(runner) {
    runner.addTest('Email validator works', () => {
        assert(Validator.email('test@email.com'), 'Valid email failed');
        assert(!Validator.email('invalid'), 'Invalid email passed');
    });

    runner.addTest('Phone validator works', () => {
        assert(Validator.phone('0912345678'), 'Valid phone failed');
        assert(!Validator.phone('12345'), 'Invalid phone passed');
    });

    runner.addTest('Password validator works', () => {
        assert(Validator.password('Password123!'), 'Valid password failed');
        assert(!Validator.password('weak'), 'Weak password passed');
    });

    runner.addTest('Username validator works', () => {
        assert(Validator.username('valid_user'), 'Valid username failed');
        assert(!Validator.username('ab'), 'Invalid username passed');
    });
}

// ============================================
// Responsive Tests
// ============================================
function responsiveTests(runner) {
    runner.addTest('Sidebar exists', () => {
        const sidebar = document.getElementById('sidebar');
        assert(sidebar !== null, 'Sidebar not found');
    });

    runner.addTest('Main content exists', () => {
        const content = document.getElementById('mainContent');
        assert(content !== null, 'Main content not found');
    });

    runner.addTest('Footer exists', () => {
        const footer = document.querySelector('.footer');
        assert(footer !== null, 'Footer not found');
    });

    runner.addTest('Navbar exists', () => {
        const navbar = document.querySelector('.navbar');
        assert(navbar !== null, 'Navbar not found');
    });
}

// ============================================
// API Tests
// ============================================
function apiTests(runner) {
    runner.addTest('API client initialized', () => {
        assert(window.STTIMS_API !== undefined, 'API client not initialized');
    });

    runner.addTest('API has auth endpoints', () => {
        assert(STTIMS_API.AuthAPI !== undefined, 'Auth endpoints missing');
    });

    runner.addTest('API has trainee endpoints', () => {
        assert(STTIMS_API.TraineeAPI !== undefined, 'Trainee endpoints missing');
    });
}

// ============================================
// Run All Tests
// ============================================
function runAllTests() {
    const runner = new TestRunner();

    // Navigation Tests
    navigationTests(runner);

    // Login Tests (only on login page)
    if (document.getElementById('loginForm')) {
        loginTests(runner);
    }

    // Dashboard Tests (only on dashboard)
    if (document.getElementById('enrollmentChart')) {
        dashboardTests(runner);
    }

    // Table Tests for common tables
    if (document.getElementById('usersTable')) {
        tableTests(runner, 'usersTable');
    }
    if (document.getElementById('traineesTable')) {
        tableTests(runner, 'traineesTable');
    }
    if (document.getElementById('instructorsTable')) {
        tableTests(runner, 'instructorsTable');
    }
    if (document.getElementById('coursesTable')) {
        tableTests(runner, 'coursesTable');
    }
    if (document.getElementById('batchesTable')) {
        tableTests(runner, 'batchesTable');
    }

    // Form Tests
    if (document.getElementById('traineeForm')) {
        formTests(runner, 'traineeForm', [
            'firstName', 'lastName', 'email', 'phone', 'gender', 'dateOfBirth',
            'guardianName', 'relationship', 'guardianPhone'
        ]);
    }

    if (document.getElementById('userForm')) {
        formTests(runner, 'userForm', ['username', 'email', 'password', 'role']);
    }

    // Modal Tests
    if (document.getElementById('addTraineeModal')) {
        modalTests(runner, 'addTraineeModal');
    }

    // Validation Tests
    validationTests(runner);

    // Responsive Tests
    responsiveTests(runner);

    // API Tests
    apiTests(runner);

    // Run tests
    runner.run();
}

// ============================================
// Run on page load if test mode is enabled
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    // Check for test mode (URL param ?test=true)
    const params = new URLSearchParams(window.location.search);
    if (params.get('test') === 'true') {
        runAllTests();
    }
});

// ============================================
// Export test runner
// ============================================
window.TestRunner = TestRunner;
window.runAllTests = runAllTests;

// ============================================
// Usage: Open any page with ?test=true to run tests
// Example: http://localhost:8000/pages/trainees.html?test=true
// ============================================
