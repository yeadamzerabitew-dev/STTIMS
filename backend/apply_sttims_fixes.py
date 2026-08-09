#!/usr/bin/env python3
"""
STTIMS fix script.
Run from two locations:
    cd ~/Documents/sttims && python3 apply_sttims_fixes.py backend
    cd ~/Documents/sttims-frontend && python3 apply_sttims_fixes.py frontend

Applies exact, targeted string replacements. If a pattern isn't found
(because your file already differs), it prints a warning and skips that
one fix instead of guessing.
"""
import sys
import os

def patch_file(path, replacements, label):
    if not os.path.exists(path):
        print(f"  [SKIP] {path} not found")
        return
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    changed = False
    for old, new, desc in replacements:
        count = content.count(old)
        if count == 0:
            print(f"  [WARN] {path}: pattern not found for '{desc}' (already patched, or file differs)")
            continue
        if count > 1:
            print(f"  [WARN] {path}: pattern for '{desc}' appears {count} times, replacing all")
        content = content.replace(old, new)
        changed = True
        print(f"  [OK]   {path}: {desc}")
    if changed:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

def backend():
    base = "."
    print("== Backend fixes ==")

    patch_file(f"{base}/models/category.py", [
        ("remote_side=[parent_category_id]", "remote_side=[category_id]",
         "fix self-referencing category relationship"),
    ], "category model")

    simple_list_fixes = {
        "controllers/trainee_controller.py": [
            ("'trainees': [trainee.to_dict() for trainee in trainees.items],",
             "'data': [trainee.to_dict() for trainee in trainees.items],", "list key -> data"),
            ("'pages': trainees.pages,", "'total_pages': trainees.pages,", "pages -> total_pages"),
        ],
        "controllers/user_controller.py": [
            ("'users': [user.to_dict_minimal() for user in users.items],",
             "'data': [user.to_dict_minimal() for user in users.items],", "list key -> data"),
            ("'pages': users.pages,", "'total_pages': users.pages,", "pages -> total_pages"),
        ],
        "controllers/course_controller.py": [
            ("'courses': [course.to_dict() for course in courses.items],",
             "'data': [course.to_dict() for course in courses.items],", "list key -> data"),
            ("'pages': courses.pages,", "'total_pages': courses.pages,", "pages -> total_pages"),
        ],
        "controllers/batch_controller.py": [
            ("'batches': [batch.to_dict() for batch in batches.items],",
             "'data': [batch.to_dict() for batch in batches.items],", "list key -> data"),
            ("'pages': batches.pages,", "'total_pages': batches.pages,", "pages -> total_pages"),
        ],
        "controllers/enrollment_controller.py": [
            ("'enrollments': [enrollment.to_dict() for enrollment in enrollments.items],",
             "'data': [enrollment.to_dict() for enrollment in enrollments.items],", "list key -> data"),
            ("'pages': enrollments.pages,", "'total_pages': enrollments.pages,", "pages -> total_pages"),
        ],
        "controllers/instructor_controller.py": [
            ("'instructors': [instructor.to_dict() for instructor in instructors.items],",
             "'data': [instructor.to_dict() for instructor in instructors.items],", "list key -> data"),
            ("'pages': instructors.pages,", "'total_pages': instructors.pages,", "pages -> total_pages"),
        ],
        "controllers/session_controller.py": [
            ("'sessions': [session.to_dict() for session in sessions.items],",
             "'data': [session.to_dict() for session in sessions.items],", "list key -> data"),
            ("'pages': sessions.pages", "'total_pages': sessions.pages", "pages -> total_pages"),
        ],
        "controllers/certificate_controller.py": [
            ("'certificates': [cert.to_dict() for cert in certificates.items],",
             "'data': [cert.to_dict() for cert in certificates.items],", "list key -> data"),
            ("'pages': certificates.pages", "'total_pages': certificates.pages", "pages -> total_pages"),
        ],
        "controllers/assessment_controller.py": [
            ("'assessments': [assessment.to_dict() for assessment in assessments.items],",
             "'data': [assessment.to_dict() for assessment in assessments.items],", "list key -> data"),
            ("'pages': assessments.pages,", "'total_pages': assessments.pages,", "pages -> total_pages"),
        ],
        "controllers/result_controller.py": [
            ("'results': results_list", "'data': results_list", "assessment-results key -> data"),
        ],
        "controllers/attendance_controller.py": [
            ("'attendance': attendance_list", "'data': attendance_list", "session-attendance key -> data"),
        ],
    }

    for path, repls in simple_list_fixes.items():
        patch_file(f"{base}/{path}", repls, path)

def frontend():
    base = "."
    print("== Frontend fixes ==")

    patch_file(f"{base}/pages/results.html", [
        ("apiCall('/grade-scale')", "apiCall('/results/grade-scale')", "grade-scale URL"),
        ("apiCall(`/assessments/${assessmentId}/results`)",
         "apiCall(`/results/assessment/${assessmentId}`)", "assessment results GET URL"),
        ("apiCall(`/enrollments/batch/${batchId}`)",
         "apiCall(`/enrollments?batch_id=${batchId}&per_page=1000`)", "enrollments by batch URL"),
        ("existing ? existing.feedback : ''",
         "existing ? existing.instructor_feedback : ''", "read instructor_feedback field"),
        ("feedback: r.feedback || ''",
         "instructor_feedback: r.feedback || ''", "send instructor_feedback field"),
        ("await apiCall(`/assessments/${currentAssessmentId}/results`, 'POST', {\n                    results: results\n                });",
         "await apiCall(`/results/bulk`, 'POST', {\n                    assessment_id: currentAssessmentId,\n                    results: results\n                });",
         "save-results POST URL + payload"),
    ], "results.html")

    patch_file(f"{base}/pages/attendance.html", [
        ("apiCall(`/sessions/batch/${batchId}`)",
         "apiCall(`/sessions?batch_id=${batchId}&per_page=1000`)", "sessions by batch URL"),
        ("apiCall(`/enrollments/batch/${batchId}`)",
         "apiCall(`/enrollments?batch_id=${batchId}&per_page=1000`)", "enrollments by batch URL"),
        ("apiCall(`/sessions/${sessionId}/attendance`)",
         "apiCall(`/attendance/session/${sessionId}`)", "get session attendance URL"),
        ("await apiCall(`/sessions/${currentSessionId}/attendance`, 'POST', {\n                    attendance: markedAttendance\n                });",
         "await apiCall(`/attendance/bulk`, 'POST', {\n                    session_id: currentSessionId,\n                    attendance: markedAttendance\n                });",
         "save attendance POST URL + payload"),
    ], "attendance.html")

    patch_file(f"{base}/pages/reports.html", [
        ("apiCall('/reports/enrollment')", "apiCall('/reports/course-enrollment')", "enrollment report URL"),
        ("apiCall('/reports/assessment')", "apiCall('/reports/assessment-results')", "assessment report URL"),
        ("apiCall('/reports/revenue')", "apiCall('/reports/payment-status')", "revenue report URL"),
        ("apiCall('/reports/certificate')", "apiCall('/reports/certificates')", "certificate report URL"),
        ("apiCall('/reports/instructor')", "apiCall('/reports/instructor-workload')", "instructor report URL"),
        ("apiCall('/dashboard/revenue')", "apiCall('/dashboard/stats')", "revenue count URL"),
    ], "reports.html")

    # Fix the 6 getXReport() functions to keep full response + map details
    path = f"{base}/pages/reports.html"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        old = "return result.data || {};"
        count = content.count(old)
        if count > 0:
            content = content.replace(
                old,
                "if (result) { result.details = result.data; }\n            return result || {};"
            )
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  [OK]   {path}: fixed {count} report-function return statements")
        else:
            print(f"  [WARN] {path}: 'return result.data || {{}};' not found (already patched?)")

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in ("backend", "frontend"):
        print(__doc__)
        sys.exit(1)
    if sys.argv[1] == "backend":
        backend()
    else:
        frontend()
    print("\nDone.")
