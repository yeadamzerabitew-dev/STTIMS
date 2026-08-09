"""
STTIMS - Sample Data Seeder
=============================================
This script inserts sample data using your ACTUAL SQLAlchemy models
(models/*.py), so it can never drift out of sync with your real
database schema the way a hand-written raw-SQL file can.
"""

import sys
import argparse
from datetime import date, time, datetime

from app import create_app
from models import (
    db, User, Trainee, Instructor, Category, Course, Batch,
    Enrollment, GradeScale, ClassSession, AttendanceRecord,
    Assessment, TraineeResult, Certificate, CertificateSetting,
    CourseAssignment, EmergencyContact, InstructorSpecialization,
)


def reset_data():
    """Wipe existing rows (keeps the table structure) in FK-safe order."""
    print("Clearing existing data...")
    for model in [
        Certificate, TraineeResult, AttendanceRecord, CourseAssignment,
        ClassSession, Assessment, Enrollment, Batch, CertificateSetting,
        Course, Category, InstructorSpecialization, EmergencyContact,
        User, Instructor, Trainee, GradeScale,
    ]:
        model.query.delete()
    db.session.commit()
    print("  Done.")


def seed():
    # -----------------------------------------------------------------
    # 1. GRADE SCALE
    # -----------------------------------------------------------------
    print("Seeding grade scale...")
    grades = [
        ("A+", 4.00, 90.00, 100.00, "Exceptional", True, 1),
        ("A", 4.00, 85.00, 89.99, "Excellent", True, 2),
        ("A-", 3.75, 80.00, 84.99, "Very Good", True, 3),
        ("B+", 3.50, 75.00, 79.99, "Good Plus", True, 4),
        ("B", 3.00, 70.00, 74.99, "Good", True, 5),
        ("B-", 2.75, 65.00, 69.99, "Above Average", True, 6),
        ("C+", 2.50, 60.00, 64.99, "Average Plus", True, 7),
        ("C", 2.00, 55.00, 59.99, "Average", True, 8),
        ("C-", 1.75, 50.00, 54.99, "Below Average", True, 9),
        ("D", 1.00, 45.00, 49.99, "Marginal Pass", True, 10),
        ("F", 0.00, 0.00, 44.99, "Fail", False, 11),
    ]
    for letter, point, mn, mx, desc, is_pass, order in grades:
        if not GradeScale.query.filter_by(grade_letter=letter).first():
            db.session.add(GradeScale(
                grade_letter=letter, grade_point=point, min_percentage=mn,
                max_percentage=mx, description=desc, is_pass=is_pass,
                display_order=order,
            ))
    db.session.commit()

    # -----------------------------------------------------------------
    # 2. CATEGORIES
    # -----------------------------------------------------------------
    print("Seeding categories...")
    cat_data = [
        ("Information Technology", "IT", "Computer and Information Technology Courses", "fa-laptop", 1),
        ("Electrical Engineering", "EE", "Electrical and Electronics Engineering", "fa-bolt", 2),
        ("Mechanical Engineering", "ME", "Mechanical Engineering and Design", "fa-cogs", 3),
        ("Software Engineering", "SE", "Software Development and Programming", "fa-code", 4),
        ("Data Science", "DS", "Data Analytics and Machine Learning", "fa-database", 5),
        ("Business Management", "BM", "Business and Management Courses", "fa-briefcase", 6),
    ]
    categories = {}
    for name, code, desc, icon, order in cat_data:
        cat = Category.query.filter_by(category_code=code).first()
        if not cat:
            cat = Category(category_name=name, category_code=code, description=desc,
                            icon=icon, display_order=order, status="Active")
            db.session.add(cat)
            db.session.flush()
        categories[code] = cat
    db.session.commit()

    # -----------------------------------------------------------------
    # 3. COURSES
    # -----------------------------------------------------------------
    print("Seeding courses...")
    course_data = [
        ("C101", "Python Programming Fundamentals", "IT",
         "Comprehensive Python programming course from basics to advanced concepts.",
         "Master Python syntax, understand OOP concepts, work with libraries, build applications",
         40, 8, 2500.00, 30, "Beginner"),
        ("C102", "Electrical Safety and Standards", "EE",
         "Essential safety practices in electrical engineering covering regulations and hazard prevention.",
         "Understand safety regulations, identify hazards, implement prevention measures",
         30, 6, 1800.00, 25, "Intermediate"),
        ("C103", "Web Development with PHP", "SE",
         "Build dynamic websites using PHP, MySQL, and modern web technologies.",
         "Understand PHP syntax, integrate with MySQL, use MVC frameworks",
         50, 10, 3500.00, 25, "Intermediate"),
        ("C104", "Project Management Fundamentals", "BM",
         "Essential project management skills including planning, execution, monitoring, and closing.",
         "Plan projects, manage resources, track progress, close projects",
         35, 7, 2000.00, 30, "Beginner"),
        ("C105", "Machine Learning Basics", "DS",
         "Introduction to machine learning concepts including supervised and unsupervised learning.",
         "Understand ML algorithms, implement solutions, evaluate models",
         45, 9, 4000.00, 20, "Advanced"),
        ("C106", "AutoCAD for Engineers", "ME",
         "Master AutoCAD for engineering design including 2D and 3D modeling.",
         "Create 2D drawings, develop 3D models, produce technical documentation",
         40, 8, 2800.00, 25, "Intermediate"),
    ]
    courses = {}
    for code, title, cat_code, desc, objectives, hrs, wks, fee, cap, level in course_data:
        c = Course.query.filter_by(course_code=code).first()
        if not c:
            c = Course(course_code=code, course_title=title, category_id=categories[cat_code].category_id,
                       description=desc, learning_objectives=objectives, duration_hours=hrs,
                       duration_weeks=wks, fee_amount=fee, fee_currency="ETB", max_capacity=cap,
                       course_level=level, certification_available=True, status="Active")
            db.session.add(c)
            db.session.flush()
        courses[code] = c
    db.session.commit()

    # -----------------------------------------------------------------
    # 4. CERTIFICATE SETTINGS
    # -----------------------------------------------------------------
    print("Seeding certificate settings...")
    if not CertificateSetting.query.filter_by(setting_name="Default Certificate").first():
        db.session.add(CertificateSetting(
            setting_name="Default Certificate", course_id=None, template_style="Professional",
            certificate_title="Certificate of Completion",
            body_text="This certificate is proudly presented to {trainee_name} for successfully "
                       "completing the {course_title} training program.",
            signature_1_name="Dr. Abebe Kebede", signature_1_title="Director of Training, STTI",
            border_style="Classic", font_family="Times New Roman", font_size="12pt",
            is_default=True, status="Active",
        ))
    db.session.commit()
    default_template = CertificateSetting.query.filter_by(is_default=True).first()

    # -----------------------------------------------------------------
    # 5. TRAINEES
    # -----------------------------------------------------------------
    print("Seeding trainees...")
    trainee_data = [
        ("T-2024-001", "Abebe", "Kebede", "Tesfaye", date(1998, 5, 15), "Male",
         "abebe.tesfaye@email.com", "0912345678", "Bole Road, Addis Ababa", "Addis Ababa",
         "BSc", "Engineer", "ABC Construction", "Worku Tesfaye", "0912345680"),
        ("T-2024-002", "Birtukan", "Hailu", "Wolde", date(1999, 8, 22), "Female",
         "birtukan.wolde@email.com", "0923456789", "Kazanchis, Addis Ababa", "Addis Ababa",
         "BSc", "Student", "AASTU", "Hailu Wolde", "0923456790"),
        ("T-2024-003", "Chala", "Dereje", "Hailu", date(1997, 11, 3), "Male",
         "chala.hailu@email.com", "0934567890", "Piassa, Addis Ababa", "Addis Ababa",
         "MSc", "Consultant", "Tech Consulting", "Dereje Hailu", "0934567892"),
        ("T-2024-004", "Desta", "Alemayehu", "Bekele", date(2000, 3, 10), "Male",
         "desta.bekele@email.com", "0945678901", "Mexico, Addis Ababa", "Addis Ababa",
         "High School", "Student", "Entoto High School", "Alemayehu Bekele", "0945678902"),
        ("T-2024-005", "Emebet", "Tesfaye", "Girma", date(1996, 7, 25), "Female",
         "emebet.girma@email.com", "0956789012", "CMC, Addis Ababa", "Addis Ababa",
         "Diploma", "Technician", "Ethio Telecom", "Tesfaye Girma", "0956789014"),
        ("T-2024-006", "Fikre", "Mekonnen", "Ayele", date(1998, 9, 12), "Male",
         "fikre.ayele@email.com", "0967890123", "Gerji, Addis Ababa", "Addis Ababa",
         "BSc", "Developer", "SofTech Solutions", "Mekonnen Ayele", "0967890124"),
        ("T-2024-007", "Genet", "Belay", "Assefa", date(1999, 12, 1), "Female",
         "genet.assefa@email.com", "0978901234", "Jemo, Addis Ababa", "Addis Ababa",
         "BSc", "Student", "AASTU", "Belay Assefa", "0978901236"),
        ("T-2024-008", "Hailu", "Girma", "Seyoum", date(1997, 4, 18), "Male",
         "hailu.seyoum@email.com", "0989012345", "Ayer Tena, Addis Ababa", "Addis Ababa",
         "MSc", "Project Manager", "Global Tech", "Girma Seyoum", "0989012346"),
        ("T-2024-009", "Iman", "Hussein", "Ali", date(1995, 6, 30), "Female",
         "iman.ali@email.com", "0990123456", "Addis Ketema, Addis Ababa", "Addis Ababa",
         "BSc", "Analyst", "DataCore Inc", "Hussein Ali", "0990123458"),
        ("T-2024-010", "Jemal", "Ahmed", "Hassan", date(1996, 10, 5), "Male",
         "jemal.hassan@email.com", "0911234567", "Koyefeche, Addis Ababa", "Addis Ababa",
         "BSc", "Engineer", "SolarTech", "Ahmed Hassan", "0911234568"),
    ]
    trainees = {}
    for code, fn, mn, ln, dob, gender, email, phone, addr, city, edu, occ, org, ec_name, ec_phone in trainee_data:
        t = Trainee.query.filter_by(trainee_code=code).first()
        if not t:
            t = Trainee(trainee_code=code, first_name=fn, middle_name=mn, last_name=ln,
                        date_of_birth=dob, gender=gender, email=email, phone_number=phone,
                        address=addr, city=city, state_region="Addis Ababa", country="Ethiopia",
                        educational_level=edu, occupation=occ, organization=org,
                        emergency_contact_name=ec_name, emergency_contact_phone=ec_phone,
                        status="Active")
            db.session.add(t)
            db.session.flush()
        trainees[code] = t
    db.session.commit()

    # -----------------------------------------------------------------
    # 6. EMERGENCY CONTACTS
    # -----------------------------------------------------------------
    print("Seeding emergency contacts...")
    for code, t in trainees.items():
        if not EmergencyContact.query.filter_by(trainee_id=t.trainee_id, is_primary=True).first():
            db.session.add(EmergencyContact(
                trainee_id=t.trainee_id, guardian_name=t.emergency_contact_name,
                relationship="Father", phone=t.emergency_contact_phone, is_primary=True,
            ))
    db.session.commit()

    # -----------------------------------------------------------------
    # 7. INSTRUCTORS
    # -----------------------------------------------------------------
    print("Seeding instructors...")
    instructor_data = [
        ("INS-001", "Abebe", "Kebede", "Teshome", date(1975, 3, 15), "Male",
         "abebe.teshome@univ.edu", "0911234567", "PhD in Computer Science, University of Oxford",
         18, "Full Time", date(2010, 1, 1), "IT"),
        ("INS-002", "Tigist", "Hailu", "Wolde", date(1980, 7, 20), "Female",
         "tigist.wolde@univ.edu", "0922345678", "PhD in Electrical Engineering, MIT",
         15, "Full Time", date(2012, 6, 1), "Electrical"),
        ("INS-003", "Chalachew", "Mekonnen", "Assefa", date(1982, 11, 10), "Male",
         "chalachew.assefa@univ.edu", "0933456789", "MSc in Software Engineering, AASTU",
         12, "Full Time", date(2015, 9, 1), "Software"),
        ("INS-004", "Kidist", "Lemma", "Tadesse", date(1985, 5, 25), "Female",
         "kidist.tadesse@univ.edu", "0944567890", "MBA in Project Management, Addis Ababa University",
         10, "Full Time", date(2016, 3, 1), "Business"),
        ("INS-005", "Yonas", "Tesfaye", "Girma", date(1978, 9, 30), "Male",
         "yonas.girma@univ.edu", "0955678901", "PhD in Statistics, University of California",
         14, "Full Time", date(2013, 8, 1), "Data"),
        ("INS-006", "Marta", "Belay", "Demissie", date(1983, 12, 15), "Female",
         "marta.demissie@univ.edu", "0966789012", "MSc in Mechanical Engineering, AASTU",
         11, "Full Time", date(2017, 1, 15), "Mechanical"),
    ]
    instructors = {}
    for code, fn, mn, ln, dob, gender, email, phone, qual, exp, emp_type, join_date, dept in instructor_data:
        i = Instructor.query.filter_by(instructor_code=code).first()
        if not i:
            i = Instructor(instructor_code=code, first_name=fn, middle_name=mn, last_name=ln,
                           date_of_birth=dob, gender=gender, email=email, phone_number=phone,
                           qualification=qual, years_of_experience=exp, employment_type=emp_type,
                           joining_date=join_date, department=dept, status="Active")
            db.session.add(i)
            db.session.flush()
        instructors[code] = i
    db.session.commit()

    # -----------------------------------------------------------------
    # 8. INSTRUCTOR SPECIALIZATIONS
    # -----------------------------------------------------------------
    print("Seeding instructor specializations...")
    spec_data = [
        ("INS-001", "Python Programming", 15, "Expert", True),
        ("INS-001", "Machine Learning", 10, "Advanced", False),
        ("INS-002", "Power Systems", 12, "Expert", True),
        ("INS-002", "Electrical Safety", 10, "Advanced", False),
        ("INS-003", "PHP Development", 10, "Expert", True),
        ("INS-004", "Project Planning", 8, "Expert", True),
        ("INS-005", "Machine Learning", 10, "Expert", True),
        ("INS-006", "AutoCAD", 8, "Expert", True),
    ]
    for code, skill, exp, level, primary in spec_data:
        inst = instructors[code]
        if not InstructorSpecialization.query.filter_by(instructor_id=inst.instructor_id, skill_name=skill).first():
            db.session.add(InstructorSpecialization(
                instructor_id=inst.instructor_id, skill_name=skill, years_of_experience=exp,
                proficiency_level=level, is_primary_skill=primary,
            ))
    db.session.commit()

    # -----------------------------------------------------------------
    # 9. USERS  (admin/manager first, then instructor + trainee accounts)
    # -----------------------------------------------------------------
    print("Seeding users...")
    credentials = []

    def make_user(username, email, role, password, trainee_id=None, instructor_id=None):
        u = User.query.filter_by(username=username).first()
        if not u:
            u = User(username=username, email=email, role=role, status="Active",
                     trainee_id=trainee_id, instructor_id=instructor_id)
            u.set_password(password)
            db.session.add(u)
            db.session.flush()
        credentials.append((username, password, role))
        return u

    admin_user = make_user("admin", "admin@sttims.com", "Admin", "Admin123!")
    manager_user = make_user("manager", "manager@sttims.com", "Manager", "Manager123!")

    instructor_users = {}
    for idx, (code, inst) in enumerate(instructors.items(), start=1):
        username = f"instructor{idx}"
        instructor_users[code] = make_user(username, inst.email, "Instructor", "Instructor123!",
                                            instructor_id=inst.instructor_id)

    trainee_users = {}
    for idx, (code, tr) in enumerate(trainees.items(), start=1):
        username = f"trainee{idx}"
        trainee_users[code] = make_user(username, tr.email, "Trainee", "Trainee123!",
                                         trainee_id=tr.trainee_id)

    db.session.commit()

    # -----------------------------------------------------------------
    # 10. BATCHES  (note: Batch has NO instructor_id column anymore)
    # -----------------------------------------------------------------
    print("Seeding batches...")
    batch_data = [
        ("B-2024-001", "Python Programming - Batch 1", "C101", date(2024, 2, 1), date(2024, 3, 28),
         "Weekday", "Mon,Wed,Fri", time(9, 0), time(12, 0), "Room 101", "Main Building", 25, "Ongoing", "INS-001"),
        ("B-2024-002", "Python Programming - Batch 2", "C101", date(2024, 3, 1), date(2024, 4, 25),
         "Weekday", "Tue,Thu", time(14, 0), time(17, 0), "Room 102", "Main Building", 20, "Upcoming", "INS-001"),
        ("B-2024-003", "Electrical Safety - Batch 1", "C102", date(2024, 2, 15), date(2024, 4, 5),
         "Weekend", "Sat", time(8, 0), time(13, 0), "Room 201", "Engineering Building", 25, "Ongoing", "INS-002"),
        ("B-2024-004", "Web Development with PHP - Batch 1", "C103", date(2024, 3, 1), date(2024, 5, 10),
         "Weekday", "Mon,Wed,Fri", time(14, 0), time(17, 0), "Room 103", "Main Building", 20, "Upcoming", "INS-003"),
        ("B-2024-005", "Project Management - Batch 1", "C104", date(2024, 2, 20), date(2024, 4, 12),
         "Weekend", "Sun", time(9, 0), time(14, 0), "Room 301", "Business Building", 30, "Ongoing", "INS-004"),
        ("B-2024-006", "Machine Learning - Batch 1", "C105", date(2024, 3, 15), date(2024, 5, 23),
         "Weekday", "Tue,Thu", time(18, 0), time(21, 0), "Room 104", "Main Building", 20, "Upcoming", "INS-005"),
        ("B-2024-007", "AutoCAD - Batch 1", "C106", date(2024, 2, 10), date(2024, 4, 4),
         "Weekday", "Mon,Wed,Fri", time(10, 0), time(13, 0), "Room 202", "Engineering Building", 20, "Ongoing", "INS-006"),
    ]
    batches = {}
    batch_instructor_map = {}
    batch_course_map = {}
    for code, name, course_code, start, end, sched_type, days, stime, etime, room, bldg, cap, status, inst_code in batch_data:
        b = Batch.query.filter_by(batch_code=code).first()
        if not b:
            b = Batch(batch_code=code, batch_name=name, course_id=courses[course_code].course_id,
                      start_date=start, end_date=end, schedule_type=sched_type, schedule_days=days,
                      schedule_time=stime, schedule_end_time=etime, room_number=room, building=bldg,
                      max_capacity=cap, min_trainees_required=5, status=status)
            db.session.add(b)
            db.session.flush()
        batches[code] = b
        batch_instructor_map[code] = inst_code
        batch_course_map[code] = course_code
    db.session.commit()

    # -----------------------------------------------------------------
    # 11. COURSE ASSIGNMENTS (this is how an instructor links to a batch now)
    # -----------------------------------------------------------------
    print("Seeding course assignments...")
    for code, b in batches.items():
        inst = instructors[batch_instructor_map[code]]
        if not CourseAssignment.query.filter_by(instructor_id=inst.instructor_id, batch_id=b.batch_id).first():
            db.session.add(CourseAssignment(
                instructor_id=inst.instructor_id, batch_id=b.batch_id,
                created_by=admin_user.user_id, assignment_date=b.start_date,
                role="Primary Instructor", start_date=b.start_date, end_date=b.end_date,
                status="Active", teaching_hours=courses[batch_course_map[code]].duration_hours,
            ))
    db.session.commit()

    # -----------------------------------------------------------------
    # 12. ENROLLMENTS
    # -----------------------------------------------------------------
    print("Seeding enrollments...")
    enrollment_data = [
        ("E-2024-001", "T-2024-001", "B-2024-001", date(2024, 1, 20), "Active", "Paid", 2500.00),
        ("E-2024-002", "T-2024-002", "B-2024-001", date(2024, 1, 22), "Active", "Paid", 2400.00),
        ("E-2024-003", "T-2024-003", "B-2024-001", date(2024, 1, 25), "Active", "Pending", None),
        ("E-2024-004", "T-2024-004", "B-2024-001", date(2024, 1, 28), "Active", "Paid", 2500.00),
        ("E-2024-005", "T-2024-005", "B-2024-003", date(2024, 2, 10), "Active", "Paid", 1800.00),
        ("E-2024-006", "T-2024-006", "B-2024-003", date(2024, 2, 12), "Active", "Paid", 1750.00),
        ("E-2024-007", "T-2024-007", "B-2024-005", date(2024, 2, 18), "Active", "Paid", 2000.00),
        ("E-2024-008", "T-2024-008", "B-2024-005", date(2024, 2, 20), "Active", "Pending", None),
        ("E-2024-009", "T-2024-009", "B-2024-007", date(2024, 2, 8), "Active", "Paid", 2800.00),
        ("E-2024-010", "T-2024-010", "B-2024-007", date(2024, 2, 9), "Active", "Paid", 2700.00),
    ]
    enrollments = {}
    for number, t_code, b_code, edate, status, pstatus, amount in enrollment_data:
        e = Enrollment.query.filter_by(enrollment_number=number).first()
        if not e:
            e = Enrollment(enrollment_number=number, trainee_id=trainees[t_code].trainee_id,
                           batch_id=batches[b_code].batch_id, enrollment_date=edate, status=status,
                           payment_status=pstatus, payment_amount=amount,
                           payment_date=edate if pstatus == "Paid" else None,
                           payment_method="Bank Transfer" if pstatus == "Paid" else None,
                           final_amount=amount)
            db.session.add(e)
            db.session.flush()
        enrollments[number] = e
    db.session.commit()

    # -----------------------------------------------------------------
    # 13. CLASS SESSIONS
    # -----------------------------------------------------------------
    print("Seeding class sessions...")
    session_data = [
        ("S-2024-001", "B-2024-001", "INS-001", date(2024, 2, 1), time(9, 0), time(12, 0), "Introduction to Python", "Lecture", "Room 101", "Completed"),
        ("S-2024-002", "B-2024-001", "INS-001", date(2024, 2, 3), time(9, 0), time(12, 0), "Python Syntax and Data Types", "Lecture", "Room 101", "Completed"),
        ("S-2024-003", "B-2024-001", "INS-001", date(2024, 2, 5), time(9, 0), time(12, 0), "Control Structures", "Lecture", "Room 101", "Completed"),
        ("S-2024-004", "B-2024-003", "INS-002", date(2024, 2, 17), time(8, 0), time(13, 0), "Introduction to Electrical Safety", "Lecture", "Room 201", "Completed"),
        ("S-2024-005", "B-2024-005", "INS-004", date(2024, 2, 25), time(9, 0), time(14, 0), "Introduction to Project Management", "Lecture", "Room 301", "Completed"),
        ("S-2024-006", "B-2024-007", "INS-006", date(2024, 2, 12), time(10, 0), time(13, 0), "AutoCAD Basics and Interface", "Lecture", "Room 202", "Completed"),
    ]
    sessions = {}
    for code, b_code, inst_code, sdate, stime, etime, topic, stype, room, status in session_data:
        s = ClassSession.query.filter_by(session_code=code).first()
        if not s:
            s = ClassSession(session_code=code, batch_id=batches[b_code].batch_id,
                             instructor_id=instructors[inst_code].instructor_id, session_date=sdate,
                             start_time=stime, end_time=etime, topic_covered=topic,
                             session_type=stype, room_number=room, status=status)
            db.session.add(s)
            db.session.flush()
        sessions[code] = s
    db.session.commit()

    # -----------------------------------------------------------------
    # 14. ATTENDANCE RECORDS
    # -----------------------------------------------------------------
    print("Seeding attendance records...")
    b1_trainee_codes = ["T-2024-001", "T-2024-002", "T-2024-003", "T-2024-004"]
    statuses = ["Present", "Present", "Late", "Present"]
    for session_code in ["S-2024-001", "S-2024-002", "S-2024-003"]:
        s = sessions[session_code]
        for t_code, st in zip(b1_trainee_codes, statuses):
            if not AttendanceRecord.query.filter_by(session_id=s.session_id,
                                                      trainee_id=trainees[t_code].trainee_id).first():
                db.session.add(AttendanceRecord(
                    session_id=s.session_id, trainee_id=trainees[t_code].trainee_id,
                    recorded_by=instructor_users["INS-001"].user_id, status=st,
                    check_in_time=time(8, 55), check_out_time=time(12, 5),
                ))
    db.session.commit()

    # -----------------------------------------------------------------
    # 15. ASSESSMENTS
    # -----------------------------------------------------------------
    print("Seeding assessments...")
    assessment_data = [
        ("A-2024-001", "B-2024-001", "Quiz 1 - Python Basics", "Quiz", 20, 20, 10,
         date(2024, 2, 15), "INS-001", "Completed"),
        ("A-2024-002", "B-2024-001", "Midterm - Python Programming", "Midterm", 50, 30, 25,
         date(2024, 3, 1), "INS-001", "Completed"),
        ("A-2024-003", "B-2024-003", "Quiz - Safety Standards", "Quiz", 20, 20, 10,
         date(2024, 3, 5), "INS-002", "Completed"),
    ]
    assessments = {}
    for code, b_code, title, atype, maxm, weight, passing, adate, inst_code, status in assessment_data:
        a = Assessment.query.filter_by(assessment_code=code).first()
        if not a:
            creator = instructor_users[inst_code]
            a = Assessment(assessment_code=code, batch_id=batches[b_code].batch_id,
                           created_by=creator.user_id, title=title, assessment_type=atype,
                           max_marks=maxm, weightage_percent=weight, passing_marks=passing,
                           assessment_date=adate, status=status)
            db.session.add(a)
            db.session.flush()
        assessments[code] = a
    db.session.commit()

    # -----------------------------------------------------------------
    # 16. TRAINEE RESULTS
    # -----------------------------------------------------------------
    print("Seeding trainee results...")
    result_data = [
        ("A-2024-001", "T-2024-001", 18.00, 90.00, "A", "Pass", "INS-001"),
        ("A-2024-001", "T-2024-002", 16.00, 80.00, "A-", "Pass", "INS-001"),
        ("A-2024-001", "T-2024-003", 14.00, 70.00, "B", "Pass", "INS-001"),
        ("A-2024-002", "T-2024-001", 42.00, 84.00, "A-", "Pass", "INS-001"),
        ("A-2024-002", "T-2024-002", 38.00, 76.00, "B+", "Pass", "INS-001"),
    ]
    for a_code, t_code, marks, pct, grade, status, inst_code in result_data:
        a = assessments[a_code]
        t = trainees[t_code]
        if not TraineeResult.query.filter_by(assessment_id=a.assessment_id, trainee_id=t.trainee_id).first():
            db.session.add(TraineeResult(
                assessment_id=a.assessment_id, trainee_id=t.trainee_id,
                recorded_by=instructor_users[inst_code].user_id, marks_obtained=marks,
                percentage_score=pct, grade=grade, status=status,
            ))
    db.session.commit()

    # -----------------------------------------------------------------
    # 17. CERTIFICATES
    # -----------------------------------------------------------------
    print("Seeding certificates...")
    cert_data = [
        ("AASTU-TIMS-2024-001", "E-2024-001", "VERIFY-TOKEN-001"),
        ("AASTU-TIMS-2024-002", "E-2024-002", "VERIFY-TOKEN-002"),
    ]
    for number, enr_number, token in cert_data:
        if not Certificate.query.filter_by(certificate_number=number).first():
            enr = enrollments[enr_number]
            db.session.add(Certificate(
                certificate_number=number, verification_token=token,
                enrollment_id=enr.enrollment_id, approved_by=admin_user.user_id,
                template_id=default_template.setting_id if default_template else None,
                issue_date=date(2024, 3, 28), issue_reason="Course Completion", status="Issued",
            ))
    db.session.commit()

    print("\nAll sample data inserted successfully!\n")
    print(f"{'Username':<15}{'Password':<18}Role")
    print("-" * 45)
    for username, password, role in credentials:
        print(f"{username:<15}{password:<18}{role}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="Delete existing data before seeding")
    args = parser.parse_args()

    app = create_app()
    with app.app_context():
        db.create_all()
        if args.reset:
            reset_data()
        try:
            seed()
        except Exception as exc:
            db.session.rollback()
            print(f"\nSeeding failed, rolled back: {exc}")
            sys.exit(1)
