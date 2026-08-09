from flask import request, jsonify, send_file
from flask_login import login_required, current_user
from models import Certificate, Enrollment, CertificateSetting, User, Trainee
from models import db
from utils.decorators import admin_required, role_required
from datetime import datetime, date
import uuid
import os
import json

class CertificateController:
    """Controller for certificate management"""
    
    @staticmethod
    def generate_certificate_number():
        """Generate a unique certificate number"""
        year = datetime.now().year
        count = Certificate.query.filter(
            Certificate.certificate_number.like(f'AASTU-TIMS-{year}%')
        ).count() + 1
        return f"AASTU-TIMS-{year}-{str(count).zfill(4)}"
    
    @staticmethod
    def generate_verification_token():
        """Generate a unique verification token"""
        return str(uuid.uuid4())
    
    @staticmethod
    def check_eligibility(enrollment_id):
        """Check if a trainee is eligible for a certificate"""
        enrollment = Enrollment.query.get(enrollment_id)
        if not enrollment:
            return False, "Enrollment not found"
        
        # Check if enrollment is completed
        if enrollment.status != 'Completed':
            return False, "Enrollment is not completed"
        
        # Check attendance requirement (minimum 75%)
        if (enrollment.attendance_percentage or 0) < 75:
            return False, f"Attendance is {enrollment.attendance_percentage}%. Minimum 75% required"
        
        # Check if trainee passed all assessments
        from models import Assessment, TraineeResult
        assessments = Assessment.query.filter_by(
            batch_id=enrollment.batch_id
        ).all()
        
        if assessments:
            results = TraineeResult.query.filter(
                TraineeResult.trainee_id == enrollment.trainee_id,
                TraineeResult.assessment_id.in_([a.assessment_id for a in assessments])
            ).all()
            
            # Check if trainee has results for all assessments
            if len(results) < len(assessments):
                return False, "Not all assessments have been completed"
            
            # Check if trainee passed all assessments
            for result in results:
                if result.status == 'Fail':
                    return False, f"Failed assessment: {result.assessment.title}"
                if result.status == 'Not Attempted':
                    return False, f"Not attempted: {result.assessment.title}"
        
        return True, "Eligible for certificate"
    
    # =============================================
    # GENERATE CERTIFICATE
    # =============================================
    
    @staticmethod
    @login_required
    @role_required(['Admin', 'Manager'])
    def generate_certificate():
        """Generate a certificate for an enrollment"""
        try:
            data = request.get_json()
            
            if not data.get('enrollment_id'):
                return jsonify({'error': 'Enrollment ID is required'}), 400
            
            # Check if certificate already exists
            existing = Certificate.query.filter_by(
                enrollment_id=data['enrollment_id']
            ).first()
            if existing:
                return jsonify({
                    'error': 'Certificate already exists for this enrollment',
                    'certificate': existing.to_dict()
                }), 400
            
            # Check eligibility
            is_eligible, message = CertificateController.check_eligibility(
                data['enrollment_id']
            )
            if not is_eligible:
                return jsonify({'error': message}), 400
            
            enrollment = Enrollment.query.get(data['enrollment_id'])
            
            # Get certificate template
            template_id = data.get('template_id')
            if not template_id:
                # Use default template for the course
                template = CertificateSetting.query.filter_by(
                    course_id=enrollment.batch.course_id,
                    is_default=True
                ).first()
                if not template:
                    template = CertificateSetting.query.filter_by(
                        is_default=True
                    ).first()
                template_id = template.setting_id if template else None
            
            # Generate certificate data
            certificate_number = CertificateController.generate_certificate_number()
            verification_token = CertificateController.generate_verification_token()
            
            # Create certificate
            certificate = Certificate(
                certificate_number=certificate_number,
                enrollment_id=data['enrollment_id'],
                issue_date=date.today(),
                expiry_date=data.get('expiry_date'),
                verification_token=verification_token,
                issue_reason=data.get('issue_reason', 'Course Completion'),
                status='Issued',
                approved_by=current_user.user_id,
                template_id=template_id,
                notes=data.get('notes', '').strip() if data.get('notes') else None
            )
            
            db.session.add(certificate)
            db.session.commit()
            
            # Generate certificate data (JSON structure for frontend)
            certificate_data = CertificateController._generate_certificate_data(certificate)
            
            return jsonify({
                'message': 'Certificate generated successfully',
                'certificate': certificate.to_dict(),
                'certificate_data': certificate_data,
                'verification_url': f"/verify/{certificate.verification_token}"
            }), 201
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    @staticmethod
    def _generate_certificate_data(certificate):
        """Generate certificate data for rendering"""
        enrollment = certificate.enrollment
        trainee = enrollment.trainee
        batch = enrollment.batch
        course = batch.course
        
        # Get template settings
        template = certificate.template
        if not template:
            template = CertificateSetting.query.filter_by(is_default=True).first()
        
        data = {
            'certificate_number': certificate.certificate_number,
            'trainee_name': trainee.full_name,
            'trainee_code': trainee.trainee_code,
            'course_title': course.course_title,
            'course_code': course.course_code,
            'batch_name': batch.batch_name,
            'issue_date': certificate.issue_date.strftime('%B %d, %Y'),
            'expiry_date': certificate.expiry_date.strftime('%B %d, %Y') if certificate.expiry_date else None,
            'verification_token': certificate.verification_token,
            'grade': enrollment.grade,
            'attendance_percentage': enrollment.attendance_percentage,
            'completion_percentage': enrollment.completion_percentage
        }
        
        if template:
            data.update({
                'template_style': template.template_style,
                'certificate_title': template.certificate_title,
                'body_text': template.body_text,
                'signature_1_name': template.signature_1_name,
                'signature_1_title': template.signature_1_title,
                'signature_2_name': template.signature_2_name,
                'signature_2_title': template.signature_2_title,
                'signature_3_name': template.signature_3_name,
                'signature_3_title': template.signature_3_title,
                'border_style': template.border_style,
                'font_family': template.font_family,
                'font_size': template.font_size,
                'logo_path': template.logo_path,
                'background_image': template.background_image
            })
        
        return data
    
    # =============================================
    # GET CERTIFICATE
    # =============================================
    
    @staticmethod
    @login_required
    def get_certificate(certificate_id):
        """Get certificate details by ID"""
        try:
            certificate = Certificate.query.get(certificate_id)
            if not certificate:
                return jsonify({'error': 'Certificate not found'}), 404
            
            # Check permission
            if not (current_user.is_admin() or current_user.is_manager()):
                enrollment = certificate.enrollment
                if current_user.is_trainee() and current_user.trainee_id != enrollment.trainee_id:
                    return jsonify({'error': 'Access denied'}), 403
            
            certificate_data = CertificateController._generate_certificate_data(certificate)
            
            return jsonify({
                'certificate': certificate.to_dict(),
                'certificate_data': certificate_data
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # VERIFY CERTIFICATE (Public)
    # =============================================
    
    @staticmethod
    def verify_certificate(token):
        """Verify a certificate by token (public endpoint)"""
        try:
            certificate = Certificate.query.filter_by(
                verification_token=token
            ).first()
            
            if not certificate:
                return jsonify({'valid': False, 'error': 'Certificate not found'}), 404
            
            if certificate.status != 'Issued':
                return jsonify({
                    'valid': False,
                    'error': f'Certificate is {certificate.status.lower()}'
                }), 400
            
            # Check if expired
            if certificate.expiry_date and certificate.expiry_date < date.today():
                return jsonify({
                    'valid': False,
                    'error': 'Certificate has expired'
                }), 400
            
            enrollment = certificate.enrollment
            trainee = enrollment.trainee
            
            return jsonify({
                'valid': True,
                'certificate_number': certificate.certificate_number,
                'trainee_name': trainee.full_name,
                'course_title': enrollment.batch.course.course_title,
                'issue_date': certificate.issue_date.isoformat(),
                'expiry_date': certificate.expiry_date.isoformat() if certificate.expiry_date else None,
                'grade': enrollment.grade,
                'verification_token': certificate.verification_token
            }), 200
            
        except Exception as e:
            return jsonify({'valid': False, 'error': str(e)}), 500
    
    # =============================================
    # REVOKE CERTIFICATE
    # =============================================
    
    @staticmethod
    @login_required
    @role_required(['Admin', 'Manager'])
    def revoke_certificate(certificate_id):
        """Revoke a certificate"""
        try:
            certificate = Certificate.query.get(certificate_id)
            if not certificate:
                return jsonify({'error': 'Certificate not found'}), 404
            
            if certificate.status == 'Revoked':
                return jsonify({'error': 'Certificate is already revoked'}), 400
            
            data = request.get_json()
            certificate.status = 'Revoked'
            certificate.notes = data.get('reason', '').strip() if data.get('reason') else 'Revoked by administrator'
            db.session.commit()
            
            return jsonify({
                'message': 'Certificate revoked successfully',
                'certificate': certificate.to_dict_minimal()
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # LIST CERTIFICATES
    # =============================================
    
    @staticmethod
    @login_required
    def list_certificates():
        """List all certificates with filters"""
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 20, type=int)
            trainee_id = request.args.get('trainee_id', type=int)
            status = request.args.get('status', '')
            search = request.args.get('search', '')
            sort_by = request.args.get('sort_by', 'issue_date')
            sort_order = request.args.get('sort_order', 'desc')
            
            query = Certificate.query
            
            if trainee_id:
                query = query.join(Enrollment).filter(Enrollment.trainee_id == trainee_id)
            
            if status:
                query = query.filter(Certificate.status == status)
            
            if search:
                query = query.join(Enrollment).join(Trainee).filter(
                    (Trainee.first_name.ilike(f'%{search}%')) |
                    (Trainee.last_name.ilike(f'%{search}%')) |
                    (Certificate.certificate_number.ilike(f'%{search}%'))
                )
            
            valid_sort_fields = ['certificate_id', 'certificate_number', 'issue_date', 'status']
            if sort_by in valid_sort_fields:
                if sort_order.lower() == 'asc':
                    query = query.order_by(getattr(Certificate, sort_by).asc())
                else:
                    query = query.order_by(getattr(Certificate, sort_by).desc())
            else:
                query = query.order_by(Certificate.issue_date.desc())
            
            certificates = query.paginate(page=page, per_page=per_page, error_out=False)
            
            return jsonify({
                'data': [cert.to_dict() for cert in certificates.items],
                'total': certificates.total,
                'page': certificates.page,
                'per_page': certificates.per_page,
                'total_pages': certificates.pages
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # GET ELIGIBLE ENROLLMENTS
    # =============================================
    
    @staticmethod
    @login_required
    @role_required(['Admin', 'Manager'])
    def get_eligible_enrollments():
        """Get enrollments eligible for certificate"""
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 20, type=int)
            
            # Get completed enrollments without certificates
            query = Enrollment.query.filter_by(status='Completed').filter(
                ~Enrollment.enrollment_id.in_(
                    db.session.query(Certificate.enrollment_id)
                )
            )
            
            # Filter by attendance
            query = query.filter(Enrollment.attendance_percentage >= 75)
            
            enrollments = query.paginate(page=page, per_page=per_page, error_out=False)
            
            eligible_list = []
            for enrollment in enrollments.items:
                is_eligible, message = CertificateController.check_eligibility(
                    enrollment.enrollment_id
                )
                if is_eligible:
                    eligible_list.append({
                        'enrollment_id': enrollment.enrollment_id,
                        'trainee_name': enrollment.trainee.full_name,
                        'trainee_code': enrollment.trainee.trainee_code,
                        'course_title': enrollment.batch.course.course_title,
                        'batch_name': enrollment.batch.batch_name,
                        'grade': enrollment.grade,
                        'attendance_percentage': enrollment.attendance_percentage,
                        'completion_percentage': enrollment.completion_percentage
                    })
            
            return jsonify({
                'eligible_enrollments': eligible_list,
                'total': len(eligible_list)
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # GET CERTIFICATE STATISTICS
    # =============================================
    
    @staticmethod
    @login_required
    @role_required(['Admin', 'Manager'])
    def get_certificate_stats():
        """Get certificate statistics"""
        try:
            total = Certificate.query.count()
            issued = Certificate.query.filter_by(status='Issued').count()
            revoked = Certificate.query.filter_by(status='Revoked').count()
            expired = Certificate.query.filter_by(status='Expired').count()
            pending = Certificate.query.filter_by(status='Pending').count()
            
            # Certificates by course
            course_stats = {}
            certificates = Certificate.query.all()
            for cert in certificates:
                course_name = cert.enrollment.batch.course.course_title
                course_stats[course_name] = course_stats.get(course_name, 0) + 1
            
            return jsonify({
                'total_certificates': total,
                'issued': issued,
                'revoked': revoked,
                'expired': expired,
                'pending': pending,
                'by_course': course_stats
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
