# STTIMS Testing Plan
## Short-Term Training Institution Management System

### 1. Test Overview

| Aspect | Details |
|--------|---------|
| **Application** | STTIMS Frontend |
| **Testing Type** | Manual & Automated Functional Testing |
| **Environment** | Local Development (http://localhost:8000) |
| **Browser** | Chrome 90+, Firefox 88+, Safari 14+ |
| **Device** | Desktop, Tablet, Mobile |

---

### 2. Test Scope

| Module | Pages | Priority |
|--------|-------|----------|
| Authentication | Login | High |
| Dashboard | Dashboard | High |
| User Management | Users | High |
| Trainee Management | Trainees | High |
| Instructor Management | Instructors | High |
| Category Management | Categories | High |
| Course Management | Courses | High |
| Batch Management | Batches | High |
| Enrollment Management | Enrollments | High |
| Attendance Management | Attendance | High |
| Session Management | Sessions | High |
| Assessment Management | Assessments | High |
| Results Management | Results | High |
| Certificate Management | Certificates | High |
| Reports | Reports | Medium |
| Settings | Settings | Medium |

---

### 3. Test Cases

#### 3.1 Navigation Testing

| Test ID | Test Case | Steps | Expected Result | Status |
|---------|-----------|-------|-----------------|--------|
| NAV-01 | Sidebar Navigation | Click each sidebar link | Correct page loads | ⬜ |
| NAV-02 | Brand Logo Click | Click STTIMS logo | Navigate to dashboard | ⬜ |
| NAV-03 | Notifications | Click notification bell | Dropdown shows notifications | ⬜ |
| NAV-04 | Profile Dropdown | Click profile avatar | Dropdown shows profile options | ⬜ |
| NAV-05 | Logout | Click Logout | Redirect to login page | ⬜ |
| NAV-06 | Mobile Sidebar | Click hamburger menu | Sidebar opens on mobile | ⬜ |
| NAV-07 | Breadcrumb | Click breadcrumb links | Navigate correctly | ⬜ |

#### 3.2 Login Page Testing

| Test ID | Test Case | Steps | Expected Result | Status |
|---------|-----------|-------|-----------------|--------|
| LOG-01 | Valid Login | Enter valid credentials, click Login | Redirect to dashboard | ⬜ |
| LOG-02 | Invalid Username | Enter invalid username, valid password | Show error message | ⬜ |
| LOG-03 | Invalid Password | Enter valid username, invalid password | Show error message | ⬜ |
| LOG-04 | Empty Fields | Submit empty form | Show validation errors | ⬜ |
| LOG-05 | Remember Me | Check remember me, login | User persists after browser close | ⬜ |
| LOG-06 | Forgot Password | Click forgot password link | Show password reset option | ⬜ |
| LOG-07 | Password Toggle | Click eye icon | Password visibility toggles | ⬜ |
| LOG-08 | Enter Key | Press Enter in password field | Form submits | ⬜ |

#### 3.3 Dashboard Testing

| Test ID | Test Case | Steps | Expected Result | Status |
|---------|-----------|-------|-----------------|--------|
| DASH-01 | Statistics Cards | Load dashboard | All cards show correct numbers | ⬜ |
| DASH-02 | Charts Load | Load dashboard | Charts render correctly | ⬜ |
| DASH-03 | Recent Activity | Load dashboard | Activity feed shows recent events | ⬜ |
| DASH-04 | Quick Actions | Click quick action buttons | Navigate to correct pages | ⬜ |
| DASH-05 | Responsive | Resize window | Layout adapts correctly | ⬜ |

#### 3.4 User Management Testing

| Test ID | Test Case | Steps | Expected Result | Status |
|---------|-----------|-------|-----------------|--------|
| USR-01 | List Users | Load users page | Table shows users | ⬜ |
| USR-02 | Add User | Fill form, click Save | User added to table | ⬜ |
| USR-03 | Edit User | Click Edit, change data, Save | User updated | ⬜ |
| USR-04 | View User | Click View | User details show | ⬜ |
| USR-05 | Delete User | Click Delete, confirm | User removed | ⬜ |
| USR-06 | Search Users | Type in search box | Table filters | ⬜ |
| USR-07 | Filter by Role | Select role filter | Table filters | ⬜ |
| USR-08 | Reset Password | Click Reset Password, enter new password | Password reset | ⬜ |
| USR-09 | Pagination | Click next page | Table updates | ⬜ |
| USR-10 | Validation | Submit empty form | Show validation errors | ⬜ |
| USR-11 | Duplicate Email | Create user with existing email | Show error | ⬜ |

#### 3.5 Trainee Management Testing

| Test ID | Test Case | Steps | Expected Result | Status |
|---------|-----------|-------|-----------------|--------|
| TRN-01 | List Trainees | Load trainees page | Table shows trainees | ⬜ |
| TRN-02 | Add Trainee | Fill form, click Save | Trainee added to table | ⬜ |
| TRN-03 | Edit Trainee | Click Edit, change data, Save | Trainee updated | ⬜ |
| TRN-04 | View Trainee | Click View | Trainee details show | ⬜ |
| TRN-05 | Delete Trainee | Click Delete, confirm | Trainee removed | ⬜ |
| TRN-06 | Search Trainees | Type in search box | Table filters | ⬜ |
| TRN-07 | Filter by Status | Select status filter | Table filters | ⬜ |
| TRN-08 | Filter by Gender | Select gender filter | Table filters | ⬜ |
| TRN-09 | Image Upload | Upload profile image | Image preview shows | ⬜ |
| TRN-10 | Export CSV | Click Export | CSV downloads | ⬜ |
| TRN-11 | Pagination | Click next page | Table updates | ⬜ |
| TRN-12 | Validation | Submit empty form | Show validation errors | ⬜ |
| TRN-13 | Duplicate Email | Create trainee with existing email | Show error | ⬜ |
| TRN-14 | Phone Validation | Enter invalid phone | Show error | ⬜ |

#### 3.6 Instructor Management Testing

| Test ID | Test Case | Steps | Expected Result | Status |
|---------|-----------|-------|-----------------|--------|
| INS-01 | List Instructors | Load instructors page | Table shows instructors | ⬜ |
| INS-02 | Add Instructor | Fill form, click Save | Instructor added | ⬜ |
| INS-03 | Edit Instructor | Click Edit, change data, Save | Instructor updated | ⬜ |
| INS-04 | View Instructor | Click View | Instructor details show | ⬜ |
| INS-05 | Delete Instructor | Click Delete, confirm | Instructor removed | ⬜ |
| INS-06 | Search Instructors | Type in search box | Table filters | ⬜ |
| INS-07 | Filter by Department | Select department filter | Table filters | ⬜ |
| INS-08 | Filter by Status | Select status filter | Table filters | ⬜ |
| INS-09 | Add Skill | Enter skill, click Add | Skill added | ⬜ |
| INS-10 | Remove Skill | Click remove on skill | Skill removed | ⬜ |
| INS-11 | Toggle Primary Skill | Click star on skill | Primary skill toggles | ⬜ |
| INS-12 | Export CSV | Click Export | CSV downloads | ⬜ |

#### 3.7 Category Management Testing

| Test ID | Test Case | Steps | Expected Result | Status |
|---------|-----------|-------|-----------------|--------|
| CAT-01 | List Categories | Load categories page | Tree shows categories | ⬜ |
| CAT-02 | Add Category | Fill form, click Save | Category added | ⬜ |
| CAT-03 | Edit Category | Click Edit, change data, Save | Category updated | ⬜ |
| CAT-04 | Delete Category | Click Delete, confirm | Category removed | ⬜ |
| CAT-05 | Add Subcategory | Create category with parent | Subcategory appears under parent | ⬜ |
| CAT-06 | Expand/Collapse | Click arrow | Subcategories toggle | ⬜ |
| CAT-07 | Search Categories | Type in search box | Tree filters | ⬜ |
| CAT-08 | Filter by Status | Select status filter | Tree filters | ⬜ |
| CAT-09 | Prevent Self-Parent | Select self as parent | Show error | ⬜ |
| CAT-10 | Prevent Delete with Children | Delete category with children | Show error | ⬜ |

#### 3.8 Course Management Testing

| Test ID | Test Case | Steps | Expected Result | Status |
|---------|-----------|-------|-----------------|--------|
| CRS-01 | List Courses | Load courses page | Table shows courses | ⬜ |
| CRS-02 | Add Course | Fill form, click Save | Course added | ⬜ |
| CRS-03 | Edit Course | Click Edit, change data, Save | Course updated | ⬜ |
| CRS-04 | View Course | Click View | Course details show | ⬜ |
| CRS-05 | Delete Course | Click Delete, confirm | Course removed | ⬜ |
| CRS-06 | Search Courses | Type in search box | Table filters | ⬜ |
| CRS-07 | Filter by Category | Select category filter | Table filters | ⬜ |
| CRS-08 | Filter by Level | Select level filter | Table filters | ⬜ |
| CRS-09 | Duplicate Code | Create course with existing code | Show error | ⬜ |
| CRS-10 | Export CSV | Click Export | CSV downloads | ⬜ |

#### 3.9 Batch Management Testing

| Test ID | Test Case | Steps | Expected Result | Status |
|---------|-----------|-------|-----------------|--------|
| BCH-01 | List Batches | Load batches page | Table shows batches | ⬜ |
| BCH-02 | Add Batch | Fill form, click Save | Batch added | ⬜ |
| BCH-03 | Edit Batch | Click Edit, change data, Save | Batch updated | ⬜ |
| BCH-04 | View Batch | Click View | Batch details show | ⬜ |
| BCH-05 | Delete Batch | Click Delete, confirm | Batch removed | ⬜ |
| BCH-06 | Search Batches | Type in search box | Table filters | ⬜ |
| BCH-07 | Filter by Course | Select course filter | Table filters | ⬜ |
| BCH-08 | Filter by Status | Select status filter | Table filters | ⬜ |
| BCH-09 | Date Validation | End date before start date | Show error | ⬜ |
| BCH-10 | Capacity Bar | View occupancy | Bar shows percentage | ⬜ |
| BCH-11 | Export CSV | Click Export | CSV downloads | ⬜ |

#### 3.10 Enrollment Testing

| Test ID | Test Case | Steps | Expected Result | Status |
|---------|-----------|-------|-----------------|--------|
| ENR-01 | List Enrollments | Load enrollments page | Table shows enrollments | ⬜ |
| ENR-02 | Add Enrollment | Select trainee & batch, Save | Enrollment added | ⬜ |
| ENR-03 | Edit Enrollment | Click Edit, change data, Save | Enrollment updated | ⬜ |
| ENR-04 | View Enrollment | Click View | Enrollment details show | ⬜ |
| ENR-05 | Delete Enrollment | Click Delete, confirm | Enrollment removed | ⬜ |
| ENR-06 | Search Enrollments | Type in search box | Table filters | ⬜ |
| ENR-07 | Filter by Status | Select status filter | Table filters | ⬜ |
| ENR-08 | Filter by Payment | Select payment filter | Table filters | ⬜ |
| ENR-09 | Duplicate Enrollment | Enroll same trainee in same batch | Show error | ⬜ |
| ENR-10 | Batch Capacity | Enroll when batch full | Show error | ⬜ |
| ENR-11 | Summary Display | View enrollment summary | Shows fee, seats, etc. | ⬜ |
| ENR-12 | Export CSV | Click Export | CSV downloads | ⬜ |

#### 3.11 Attendance Testing

| Test ID | Test Case | Steps | Expected Result | Status |
|---------|-----------|-------|-----------------|--------|
| ATN-01 | Load Trainees | Select batch & session | Trainees load | ⬜ |
| ATN-02 | Mark Present | Click Present button | Status updates | ⬜ |
| ATN-03 | Mark Absent | Click Absent button | Status updates | ⬜ |
| ATN-04 | Mark Late | Click Late button | Status updates | ⬜ |
| ATN-05 | Mark Excused | Click Excused button | Status updates | ⬜ |
| ATN-06 | Toggle Status | Click same status again | Status toggles off | ⬜ |
| ATN-07 | Mark All Present | Click All Present | All marked present | ⬜ |
| ATN-08 | Reset All | Click Reset | All reset | ⬜ |
| ATN-09 | Add Remarks | Type in remarks field | Remarks saved | ⬜ |
| ATN-10 | Save Attendance | Click Save | Attendance saved | ⬜ |
| ATN-11 | Summary Updates | Mark statuses | Summary counts update | ⬜ |
| ATN-12 | Unmarked Warning | Save with unmarked trainees | Show warning | ⬜ |

#### 3.12 Assessment Testing

| Test ID | Test Case | Steps | Expected Result | Status |
|---------|-----------|-------|-----------------|--------|
| ASM-01 | List Assessments | Load assessments page | Table shows assessments | ⬜ |
| ASM-02 | Add Assessment | Fill form, click Save | Assessment added | ⬜ |
| ASM-03 | Edit Assessment | Click Edit, change data, Save | Assessment updated | ⬜ |
| ASM-04 | View Assessment | Click View | Assessment details show | ⬜ |
| ASM-05 | Delete Assessment | Click Delete, confirm | Assessment removed | ⬜ |
| ASM-06 | Weightage Validation | Total > 100% | Show error | ⬜ |
| ASM-07 | Search Assessments | Type in search box | Table filters | ⬜ |
| ASM-08 | Filter by Type | Select type filter | Table filters | ⬜ |
| ASM-09 | Filter by Status | Select status filter | Table filters | ⬜ |
| ASM-10 | Export CSV | Click Export | CSV downloads | ⬜ |

#### 3.13 Results Testing

| Test ID | Test Case | Steps | Expected Result | Status |
|---------|-----------|-------|-----------------|--------|
| RSL-01 | Load Trainees | Select assessment | Trainees load | ⬜ |
| RSL-02 | Enter Marks | Enter marks for trainee | Percentage, grade, status update | ⬜ |
| RSL-03 | Auto Fill | Click Auto Fill | All marks filled | ⬜ |
| RSL-04 | Reset All | Click Reset | All marks cleared | ⬜ |
| RSL-05 | Save Results | Click Save | Results saved | ⬜ |
| RSL-06 | Grade Display | Grade changes based on marks | Grade updates correctly | ⬜ |
| RSL-07 | Summary Updates | Enter marks | Summary counts update | ⬜ |
| RSL-08 | Add Remarks | Type in remarks field | Remarks saved | ⬜ |
| RSL-09 | Unmarked Warning | Save with unmarked trainees | Show warning | ⬜ |

#### 3.14 Certificate Testing

| Test ID | Test Case | Steps | Expected Result | Status |
|---------|-----------|-------|-----------------|--------|
| CRT-01 | List Certificates | Load certificates page | Certificates show | ⬜ |
| CRT-02 | Generate Certificate | Fill form, click Generate | Certificate added | ⬜ |
| CRT-03 | Preview Certificate | Click Preview | Certificate preview shows | ⬜ |
| CRT-04 | Print Certificate | Click Print | Print dialog opens | ⬜ |
| CRT-05 | Download PDF | Click Download PDF | PDF downloads | ⬜ |
| CRT-06 | Delete Certificate | Click Delete, confirm | Certificate removed | ⬜ |
| CRT-07 | Search Certificates | Type in search box | Grid filters | ⬜ |
| CRT-08 | Filter by Status | Select status filter | Grid filters | ⬜ |
| CRT-09 | Export CSV | Click Export | CSV downloads | ⬜ |

#### 3.15 Reports Testing

| Test ID | Test Case | Steps | Expected Result | Status |
|---------|-----------|-------|-----------------|--------|
| RPT-01 | Load Report | Click report card | Report loads | ⬜ |
| RPT-02 | Switch View | Click Summary/Details/Chart | View changes | ⬜ |
| RPT-03 | Export PDF | Click PDF | PDF downloads | ⬜ |
| RPT-04 | Export Excel | Click Excel | CSV downloads | ⬜ |
| RPT-05 | Print Report | Click Print | Print dialog opens | ⬜ |
| RPT-06 | All Report Types | Click each report card | Each report loads | ⬜ |

#### 3.16 Settings Testing

| Test ID | Test Case | Steps | Expected Result | Status |
|---------|-----------|-------|-----------------|--------|
| SET-01 | Save Institution | Fill form, click Save | Settings saved | ⬜ |
| SET-02 | Upload Logo | Upload image | Logo preview updates | ⬜ |
| SET-03 | Remove Logo | Click Remove | Logo removed | ⬜ |
| SET-04 | Select Theme | Click theme option | Theme changes | ⬜ |
| SET-05 | Select Template | Choose template | Template preview updates | ⬜ |
| SET-06 | Preview Template | Click Preview | Template preview modal shows | ⬜ |
| SET-07 | Save Email | Fill form, click Save | Email settings saved | ⬜ |
| SET-08 | Change Password | Fill form, click Change Password | Password changed | ⬜ |
| SET-09 | Password Strength | Type password | Strength indicator updates | ⬜ |

#### 3.17 Responsive Testing

| Test ID | Test Case | Steps | Expected Result | Status |
|---------|-----------|-------|-----------------|--------|
| RES-01 | Desktop View | 1920x1080 | Layout works | ⬜ |
| RES-02 | Laptop View | 1366x768 | Layout works | ⬜ |
| RES-03 | Tablet Portrait | 768x1024 | Layout works | ⬜ |
| RES-04 | Tablet Landscape | 1024x768 | Layout works | ⬜ |
| RES-05 | Mobile Large | 414x896 | Layout works | ⬜ |
| RES-06 | Mobile Medium | 375x812 | Layout works | ⬜ |
| RES-07 | Mobile Small | 320x568 | Layout works | ⬜ |
| RES-08 | Sidebar Collapse | Resize to mobile | Sidebar collapses | ⬜ |
| RES-09 | Table Card View | Resize to mobile | Tables become cards | ⬜ |
| RES-10 | Touch Targets | On mobile | Buttons are tappable | ⬜ |

---

### 4. Test Execution Log

| Date | Tester | Test Suite | Pass | Fail | Notes |
|------|--------|------------|------|------|-------|
| | | | | | |

---

### 5. Bug Tracking

| Bug ID | Page | Description | Severity | Status |
|--------|------|-------------|----------|--------|
| | | | | |

---

### 6. Sign-Off

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Developer | | | |
| Tester | | | |
| Project Lead | | | |

---
