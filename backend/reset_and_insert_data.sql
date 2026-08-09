USE sttims_db;

-- =============================================
-- CLEAR EXISTING SAMPLE DATA (FK-safe order)
-- =============================================
SET FOREIGN_KEY_CHECKS = 0;

TRUNCATE TABLE trainee_results;
TRUNCATE TABLE assessments;
TRUNCATE TABLE attendance_records;
TRUNCATE TABLE class_sessions;
TRUNCATE TABLE enrollments;
TRUNCATE TABLE users;
TRUNCATE TABLE batches;
TRUNCATE TABLE instructors;
TRUNCATE TABLE trainees;
TRUNCATE TABLE courses;
TRUNCATE TABLE categories;
TRUNCATE TABLE grade_scale;

SET FOREIGN_KEY_CHECKS = 1;

-- =============================================
-- INSERT SAMPLE DATA FOR STTIMS (FIXED VERSION)
-- =============================================

-- ---------------------------------------------
-- 1. GRADE_SCALE
-- ---------------------------------------------
INSERT INTO grade_scale (grade_letter, grade_point, min_percentage, max_percentage, description, is_pass, display_order) VALUES
('A+', 4.00, 90.00, 100.00, 'Exceptional', 1, 1),
('A', 4.00, 85.00, 89.99, 'Excellent', 1, 2),
('A-', 3.75, 80.00, 84.99, 'Very Good', 1, 3),
('B+', 3.50, 75.00, 79.99, 'Good Plus', 1, 4),
('B', 3.00, 70.00, 74.99, 'Good', 1, 5),
('B-', 2.75, 65.00, 69.99, 'Above Average', 1, 6),
('C+', 2.50, 60.00, 64.99, 'Average Plus', 1, 7),
('C', 2.00, 55.00, 59.99, 'Average', 1, 8),
('C-', 1.75, 50.00, 54.99, 'Below Average', 1, 9),
('D', 1.00, 45.00, 49.99, 'Marginal Pass', 1, 10),
('F', 0.00, 0.00, 44.99, 'Fail', 0, 11);

-- ---------------------------------------------
-- 2. CATEGORIES
-- ---------------------------------------------
INSERT INTO categories (category_name, category_code, description, icon, display_order, status) VALUES
('Information Technology', 'IT', 'Computer and Information Technology Courses', 'fa-laptop', 1, 'Active'),
('Electrical Engineering', 'EE', 'Electrical and Electronics Engineering', 'fa-bolt', 2, 'Active'),
('Mechanical Engineering', 'ME', 'Mechanical Engineering and Design', 'fa-cogs', 3, 'Active'),
('Software Engineering', 'SE', 'Software Development and Programming', 'fa-code', 4, 'Active'),
('Data Science', 'DS', 'Data Analytics and Machine Learning', 'fa-database', 5, 'Active'),
('Business Management', 'BM', 'Business and Management Courses', 'fa-briefcase', 6, 'Active');

-- ---------------------------------------------
-- 3. COURSES
-- ---------------------------------------------
INSERT INTO courses (
    course_code, course_title, category_id, description,
    duration_hours, duration_weeks, fee_amount, fee_currency,
    max_capacity, course_level, certification_available, status
) VALUES
('C101', 'Python Programming Fundamentals', 1,
 'Comprehensive Python programming course from basics to advanced concepts.',
 40, 8, 2500.00, 'ETB', 30, 'Beginner', 1, 'Active'),

('C102', 'Electrical Safety and Standards', 2,
 'Essential safety practices in electrical engineering covering regulations and hazard prevention.',
 30, 6, 1800.00, 'ETB', 25, 'Intermediate', 1, 'Active'),

('C103', 'Web Development with PHP', 4,
 'Build dynamic websites using PHP, MySQL, and modern web technologies.',
 50, 10, 3500.00, 'ETB', 25, 'Intermediate', 1, 'Active'),

('C104', 'Project Management Fundamentals', 6,
 'Essential project management skills including planning, execution, monitoring, and closing.',
 35, 7, 2000.00, 'ETB', 30, 'Beginner', 1, 'Active'),

('C105', 'Machine Learning Basics', 5,
 'Introduction to machine learning concepts including supervised and unsupervised learning.',
 45, 9, 4000.00, 'ETB', 20, 'Advanced', 1, 'Active'),

('C106', 'AutoCAD for Engineers', 3,
 'Master AutoCAD for engineering design including 2D and 3D modeling.',
 40, 8, 2800.00, 'ETB', 25, 'Intermediate', 1, 'Active');

-- ---------------------------------------------
-- 4. TRAINEES
-- ---------------------------------------------
INSERT INTO trainees (
    trainee_code, first_name, middle_name, last_name, date_of_birth, gender,
    email, phone_number, alternative_phone, address, city, state_region, country,
    educational_level, occupation, organization, emergency_contact_name,
    emergency_contact_phone, registration_date, status
) VALUES
('T-2024-001', 'Abebe', 'Kebede', 'Tesfaye', '1998-05-15', 'Male',
 'abebe.tesfaye@email.com', '0912345678', '0912345679',
 'Bole Road, Addis Ababa', 'Addis Ababa', 'Addis Ababa', 'Ethiopia',
 'BSc', 'Engineer', 'ABC Construction', 'Worku Tesfaye', '0912345680',
 NOW(), 'Active'),

('T-2024-002', 'Birtukan', 'Hailu', 'Wolde', '1999-08-22', 'Female',
 'birtukan.wolde@email.com', '0923456789', NULL,
 'Kazanchis, Addis Ababa', 'Addis Ababa', 'Addis Ababa', 'Ethiopia',
 'BSc', 'Student', 'AASTU', 'Hailu Wolde', '0923456790',
 NOW(), 'Active'),

('T-2024-003', 'Chala', 'Dereje', 'Hailu', '1997-11-03', 'Male',
 'chala.hailu@email.com', '0934567890', '0934567891',
 'Piassa, Addis Ababa', 'Addis Ababa', 'Addis Ababa', 'Ethiopia',
 'MSc', 'Consultant', 'Tech Consulting', 'Dereje Hailu', '0934567892',
 NOW(), 'Active'),

('T-2024-004', 'Desta', 'Alemayehu', 'Bekele', '2000-03-10', 'Male',
 'desta.bekele@email.com', '0945678901', NULL,
 'Mexico, Addis Ababa', 'Addis Ababa', 'Addis Ababa', 'Ethiopia',
 'High School', 'Student', 'Entoto High School', 'Alemayehu Bekele', '0945678902',
 NOW(), 'Active'),

('T-2024-005', 'Emebet', 'Tesfaye', 'Girma', '1996-07-25', 'Female',
 'emebet.girma@email.com', '0956789012', '0956789013',
 'CMC, Addis Ababa', 'Addis Ababa', 'Addis Ababa', 'Ethiopia',
 'Diploma', 'Technician', 'Ethio Telecom', 'Tesfaye Girma', '0956789014',
 NOW(), 'Active'),

('T-2024-006', 'Fikre', 'Mekonnen', 'Ayele', '1998-09-12', 'Male',
 'fikre.ayele@email.com', '0967890123', NULL,
 'Gerji, Addis Ababa', 'Addis Ababa', 'Addis Ababa', 'Ethiopia',
 'BSc', 'Developer', 'SofTech Solutions', 'Mekonnen Ayele', '0967890124',
 NOW(), 'Active'),

('T-2024-007', 'Genet', 'Belay', 'Assefa', '1999-12-01', 'Female',
 'genet.assefa@email.com', '0978901234', '0978901235',
 'Jemo, Addis Ababa', 'Addis Ababa', 'Addis Ababa', 'Ethiopia',
 'BSc', 'Student', 'AASTU', 'Belay Assefa', '0978901236',
 NOW(), 'Active'),

('T-2024-008', 'Hailu', 'Girma', 'Seyoum', '1997-04-18', 'Male',
 'hailu.seyoum@email.com', '0989012345', NULL,
 'Ayer Tena, Addis Ababa', 'Addis Ababa', 'Addis Ababa', 'Ethiopia',
 'MSc', 'Project Manager', 'Global Tech', 'Girma Seyoum', '0989012346',
 NOW(), 'Active'),

('T-2024-009', 'Iman', 'Hussein', 'Ali', '1995-06-30', 'Female',
 'iman.ali@email.com', '0990123456', '0990123457',
 'Addis Ketema, Addis Ababa', 'Addis Ababa', 'Addis Ababa', 'Ethiopia',
 'BSc', 'Analyst', 'DataCore Inc', 'Hussein Ali', '0990123458',
 NOW(), 'Active'),

('T-2024-010', 'Jemal', 'Ahmed', 'Hassan', '1996-10-05', 'Male',
 'jemal.hassan@email.com', '0911234567', NULL,
 'Koyefeche, Addis Ababa', 'Addis Ababa', 'Addis Ababa', 'Ethiopia',
 'BSc', 'Engineer', 'SolarTech', 'Ahmed Hassan', '0911234568',
 NOW(), 'Active');

-- ---------------------------------------------
-- 5. INSTRUCTORS
-- ---------------------------------------------
INSERT INTO instructors (
    instructor_code, first_name, middle_name, last_name, date_of_birth, gender,
    email, phone_number, address, city, qualification, years_of_experience,
    bio, status, employment_type, joining_date, department
) VALUES
('INS-001', 'Dr. Abebe', 'Kebede', 'Teshome', '1975-03-15', 'Male',
 'abebe.teshome@univ.edu', '0911234567', 'Bole, Addis Ababa', 'Addis Ababa',
 'PhD in Computer Science, University of Oxford', 18,
 'Expert in Python, Machine Learning, and Software Architecture', 'Active', 'Full Time', '2010-01-01', 'IT'),

('INS-002', 'Dr. Tigist', 'Hailu', 'Wolde', '1980-07-20', 'Female',
 'tigist.wolde@univ.edu', '0922345678', 'Kazanchis, Addis Ababa', 'Addis Ababa',
 'PhD in Electrical Engineering, MIT', 15,
 'Specialist in Power Systems, Safety Standards, and Renewable Energy', 'Active', 'Full Time', '2012-06-01', 'Electrical'),

('INS-003', 'Eng. Chalachew', 'Mekonnen', 'Assefa', '1982-11-10', 'Male',
 'chalachew.assefa@univ.edu', '0933456789', 'Piassa, Addis Ababa', 'Addis Ababa',
 'MSc in Software Engineering, AASTU', 12,
 'Full-stack developer, PHP expert, and Web Technologies specialist', 'Active', 'Full Time', '2015-09-01', 'Software'),

('INS-004', 'Ms. Kidist', 'Lemma', 'Tadesse', '1985-05-25', 'Female',
 'kidist.tadesse@univ.edu', '0944567890', 'CMC, Addis Ababa', 'Addis Ababa',
 'MBA in Project Management, Addis Ababa University', 10,
 'Project management expert with PMP certification', 'Active', 'Full Time', '2016-03-01', 'Business'),

('INS-005', 'Dr. Yonas', 'Tesfaye', 'Girma', '1978-09-30', 'Male',
 'yonas.girma@univ.edu', '0955678901', 'Gerji, Addis Ababa', 'Addis Ababa',
 'PhD in Statistics, University of California', 14,
 'Machine Learning, Data Science, and Statistical Analysis expert', 'Active', 'Full Time', '2013-08-01', 'Data'),

('INS-006', 'Eng. Marta', 'Belay', 'Demissie', '1983-12-15', 'Female',
 'marta.demissie@univ.edu', '0966789012', 'Jemo, Addis Ababa', 'Addis Ababa',
 'MSc in Mechanical Engineering, AASTU', 11,
 'AutoCAD specialist and Mechanical Design expert', 'Active', 'Full Time', '2017-01-15', 'Mechanical');

-- ---------------------------------------------
-- 6. BATCHES
-- ---------------------------------------------
INSERT INTO batches (
    batch_code, batch_name, course_id, start_date, end_date,
    schedule_type, schedule_days, schedule_time, schedule_end_time,
    room_number, building, max_capacity, min_trainees_required,
    status
) VALUES
('B-2024-001', 'Python Programming - Batch 1', 1, '2024-02-01', '2024-03-28',
 'Weekday', 'Mon,Wed,Fri', '09:00:00', '12:00:00',
 'Room 101', 'Main Building', 25, 5, 'Ongoing'),

('B-2024-002', 'Python Programming - Batch 2', 1, '2024-03-01', '2024-04-25',
 'Weekday', 'Tue,Thu', '14:00:00', '17:00:00',
 'Room 102', 'Main Building', 20, 5, 'Upcoming'),

('B-2024-003', 'Electrical Safety - Batch 1', 2, '2024-02-15', '2024-04-05',
 'Weekend', 'Sat', '08:00:00', '13:00:00',
 'Room 201', 'Engineering Building', 25, 5, 'Ongoing'),

('B-2024-004', 'Web Development with PHP - Batch 1', 3, '2024-03-01', '2024-05-10',
 'Weekday', 'Mon,Wed,Fri', '14:00:00', '17:00:00',
 'Room 103', 'Main Building', 20, 5, 'Upcoming'),

('B-2024-005', 'Project Management - Batch 1', 4, '2024-02-20', '2024-04-12',
 'Weekend', 'Sun', '09:00:00', '14:00:00',
 'Room 301', 'Business Building', 30, 5, 'Ongoing'),

('B-2024-006', 'Machine Learning - Batch 1', 5, '2024-03-15', '2024-05-23',
 'Weekday', 'Tue,Thu', '18:00:00', '21:00:00',
 'Room 104', 'Main Building', 20, 5, 'Upcoming'),

('B-2024-007', 'AutoCAD - Batch 1', 6, '2024-02-10', '2024-04-04',
 'Weekday', 'Mon,Wed,Fri', '10:00:00', '13:00:00',
 'Room 202', 'Engineering Building', 20, 5, 'Ongoing');

-- ---------------------------------------------
-- 7. USERS (moved before enrollments/sessions/assessments/results
--            since those tables have NOT NULL FKs to users.user_id)
-- ---------------------------------------------
INSERT INTO users (
    username, email, password_hash, role, trainee_id, instructor_id, status
) VALUES
('admin', 'admin@sttims.com', 'scrypt:32768:8:1$dummy$dummy_hash', 'Admin', NULL, NULL, 'Active'),
('manager', 'manager@sttims.com', 'scrypt:32768:8:1$dummy$dummy_hash', 'Manager', NULL, NULL, 'Active'),
('instructor1', 'abebe.teshome@univ.edu', 'scrypt:32768:8:1$dummy$dummy_hash', 'Instructor', NULL, 1, 'Active'),
('instructor2', 'tigist.wolde@univ.edu', 'scrypt:32768:8:1$dummy$dummy_hash', 'Instructor', NULL, 2, 'Active'),
('instructor3', 'chalachew.assefa@univ.edu', 'scrypt:32768:8:1$dummy$dummy_hash', 'Instructor', NULL, 3, 'Active'),
('trainee1', 'abebe.tesfaye@email.com', 'scrypt:32768:8:1$dummy$dummy_hash', 'Trainee', 1, NULL, 'Active'),
('trainee2', 'birtukan.wolde@email.com', 'scrypt:32768:8:1$dummy$dummy_hash', 'Trainee', 2, NULL, 'Active'),
('trainee3', 'chala.hailu@email.com', 'scrypt:32768:8:1$dummy$dummy_hash', 'Trainee', 3, NULL, 'Active'),
('trainee4', 'desta.bekele@email.com', 'scrypt:32768:8:1$dummy$dummy_hash', 'Trainee', 4, NULL, 'Active'),
('trainee5', 'emebet.girma@email.com', 'scrypt:32768:8:1$dummy$dummy_hash', 'Trainee', 5, NULL, 'Active');

-- ---------------------------------------------
-- 8. ENROLLMENTS
-- ---------------------------------------------
INSERT INTO enrollments (
    enrollment_number, trainee_id, batch_id, enrollment_date, status, payment_status,
    payment_amount, payment_date, payment_method, discount_amount, final_amount
) VALUES
('E-2024-001', 1, 1, '2024-01-20', 'Active', 'Paid', 2500.00, '2024-01-20', 'Bank Transfer', 0.00, 2500.00),
('E-2024-002', 2, 1, '2024-01-22', 'Active', 'Paid', 2500.00, '2024-01-22', 'Cash', 100.00, 2400.00),
('E-2024-003', 3, 1, '2024-01-25', 'Active', 'Pending', NULL, NULL, NULL, 0.00, NULL),
('E-2024-004', 4, 1, '2024-01-28', 'Active', 'Paid', 2500.00, '2024-01-28', 'Bank Transfer', 0.00, 2500.00),
('E-2024-005', 5, 3, '2024-02-10', 'Active', 'Paid', 1800.00, '2024-02-10', 'Cash', 0.00, 1800.00),
('E-2024-006', 6, 3, '2024-02-12', 'Active', 'Paid', 1800.00, '2024-02-12', 'Bank Transfer', 50.00, 1750.00),
('E-2024-007', 7, 5, '2024-02-18', 'Active', 'Paid', 2000.00, '2024-02-18', 'Cash', 0.00, 2000.00),
('E-2024-008', 8, 5, '2024-02-20', 'Active', 'Pending', NULL, NULL, NULL, 0.00, NULL),
('E-2024-009', 9, 7, '2024-02-08', 'Active', 'Paid', 2800.00, '2024-02-08', 'Bank Transfer', 0.00, 2800.00),
('E-2024-010', 10, 7, '2024-02-09', 'Active', 'Paid', 2800.00, '2024-02-09', 'Cash', 100.00, 2700.00),
('E-2024-011', 1, 4, '2024-02-28', 'Enrolled', 'Pending', NULL, NULL, NULL, 0.00, NULL),
('E-2024-012', 2, 6, '2024-03-10', 'Enrolled', 'Pending', NULL, NULL, NULL, 0.00, NULL);

-- ---------------------------------------------
-- 9. CLASS SESSIONS (added instructor_id - NOT NULL in schema)
-- ---------------------------------------------
INSERT INTO class_sessions (
    session_code, batch_id, session_date, start_time, end_time,
    topic_covered, session_type, instructor_id, room_number, status
) VALUES
('S-2024-001', 1, '2024-02-01', '09:00:00', '12:00:00', 'Introduction to Python', 'Lecture', 1, 'Room 101', 'Completed'),
('S-2024-002', 1, '2024-02-03', '09:00:00', '12:00:00', 'Python Syntax and Data Types', 'Lecture', 1, 'Room 101', 'Completed'),
('S-2024-003', 1, '2024-02-05', '09:00:00', '12:00:00', 'Control Structures', 'Lecture', 1, 'Room 101', 'Completed'),
('S-2024-004', 1, '2024-02-08', '09:00:00', '12:00:00', 'Functions and Modules', 'Lecture', 1, 'Room 101', 'Completed'),
('S-2024-005', 1, '2024-02-10', '09:00:00', '12:00:00', 'Object-Oriented Programming', 'Lecture', 1, 'Room 101', 'Completed'),
('S-2024-006', 1, '2024-02-12', '09:00:00', '12:00:00', 'Python Lab - Basic Exercises', 'Lab', 1, 'Room 101', 'Completed'),
('S-2024-007', 3, '2024-02-17', '08:00:00', '13:00:00', 'Introduction to Electrical Safety', 'Lecture', 2, 'Room 201', 'Completed'),
('S-2024-008', 3, '2024-02-24', '08:00:00', '13:00:00', 'Safety Standards and Regulations', 'Lecture', 2, 'Room 201', 'Completed'),
('S-2024-009', 3, '2024-03-02', '08:00:00', '13:00:00', 'Hazard Identification', 'Workshop', 2, 'Room 201', 'Completed'),
('S-2024-010', 5, '2024-02-25', '09:00:00', '14:00:00', 'Introduction to Project Management', 'Lecture', 4, 'Room 301', 'Completed'),
('S-2024-011', 5, '2024-03-03', '09:00:00', '14:00:00', 'Project Planning and Scheduling', 'Lecture', 4, 'Room 301', 'Scheduled'),
('S-2024-012', 7, '2024-02-12', '10:00:00', '13:00:00', 'AutoCAD Basics and Interface', 'Lecture', 6, 'Room 202', 'Completed'),
('S-2024-013', 7, '2024-02-14', '10:00:00', '13:00:00', '2D Drawing Fundamentals', 'Lecture', 6, 'Room 202', 'Completed'),
('S-2024-014', 7, '2024-02-16', '10:00:00', '13:00:00', 'AutoCAD Lab - Practice', 'Lab', 6, 'Room 202', 'Completed');

-- ---------------------------------------------
-- 10. ATTENDANCE RECORDS
-- ---------------------------------------------
INSERT INTO attendance_records (
    session_id, trainee_id, status, check_in_time, check_out_time, remarks, recorded_by
) VALUES
(1, 1, 'Present', '08:55:00', '12:05:00', NULL, 1),
(1, 2, 'Present', '08:58:00', '12:02:00', NULL, 1),
(1, 3, 'Late', '09:15:00', '12:00:00', 'Traffic delay', 1),
(1, 4, 'Present', '08:50:00', '12:10:00', NULL, 1),
(1, 5, 'Absent', NULL, NULL, 'Sick', 1),
(2, 1, 'Present', '08:55:00', '12:05:00', NULL, 1),
(2, 2, 'Present', '08:58:00', '12:02:00', NULL, 1),
(2, 3, 'Present', '09:00:00', '12:00:00', NULL, 1),
(2, 4, 'Present', '08:50:00', '12:10:00', NULL, 1),
(2, 5, 'Absent', NULL, NULL, 'Sick', 1);

-- ---------------------------------------------
-- 11. ASSESSMENTS (added created_by - NOT NULL in schema)
-- ---------------------------------------------
INSERT INTO assessments (
    assessment_code, batch_id, title, description, assessment_type,
    max_marks, weightage_percent, passing_marks, assessment_date,
    start_time, end_time, duration_minutes, total_questions,
    instructions, status, created_by
) VALUES
('A-2024-001', 1, 'Quiz 1 - Python Basics', 'Basic Python concepts and syntax', 'Quiz',
 20, 20, 10, '2024-02-15', '09:00:00', '09:30:00', 30, 10, 'Answer all questions', 'Completed', 3),

('A-2024-002', 1, 'Midterm - Python Programming', 'Comprehensive test on Python', 'Midterm',
 50, 30, 25, '2024-03-01', '09:00:00', '11:00:00', 120, 15, 'Choose the best answer', 'Completed', 3),

('A-2024-003', 3, 'Quiz - Safety Standards', 'Safety regulations and standards', 'Quiz',
 20, 20, 10, '2024-03-05', '10:00:00', '10:30:00', 30, 10, 'Multiple choice questions', 'Completed', 4);

-- ---------------------------------------------
-- 12. TRAINEE RESULTS
-- ---------------------------------------------
INSERT INTO trainee_results (
    assessment_id, trainee_id, marks_obtained, percentage_score, grade,
    status, comments, recorded_by
) VALUES
(1, 1, 18.00, 90.00, 'A', 'Pass', 'Excellent understanding', 3),
(1, 2, 16.00, 80.00, 'A-', 'Pass', 'Good understanding', 3),
(1, 3, 14.00, 70.00, 'B', 'Pass', 'Satisfactory', 3),
(1, 4, 12.00, 60.00, 'C+', 'Pass', 'Average', 3),
(2, 1, 42.00, 84.00, 'A-', 'Pass', 'Very good performance', 3),
(2, 2, 38.00, 76.00, 'B+', 'Pass', 'Good performance', 3),
(2, 3, 35.00, 70.00, 'B', 'Pass', 'Satisfactory', 3),
(2, 4, 28.00, 56.00, 'C', 'Pass', 'Average', 3),
(3, 5, 16.00, 80.00, 'A-', 'Pass', 'Good understanding', 4),
(3, 6, 18.00, 90.00, 'A', 'Pass', 'Excellent', 4);

-- =============================================
-- DATA VERIFICATION
-- =============================================
SELECT '========================================' AS '';
SELECT 'SAMPLE DATA INSERTION COMPLETE!' AS 'Status';
SELECT '========================================' AS '';

SELECT 'Trainees' AS 'Table', COUNT(*) AS 'Records' FROM trainees
UNION ALL
SELECT 'Instructors', COUNT(*) FROM instructors
UNION ALL
SELECT 'Courses', COUNT(*) FROM courses
UNION ALL
SELECT 'Batches', COUNT(*) FROM batches
UNION ALL
SELECT 'Enrollments', COUNT(*) FROM enrollments
UNION ALL
SELECT 'Users', COUNT(*) FROM users
UNION ALL
SELECT 'grade_scale', COUNT(*) FROM grade_scale
UNION ALL
SELECT 'assessments', COUNT(*) FROM assessments
UNION ALL
SELECT 'trainee_results', COUNT(*) FROM trainee_results;

SELECT '✅ All sample data inserted successfully!' AS 'Message';
