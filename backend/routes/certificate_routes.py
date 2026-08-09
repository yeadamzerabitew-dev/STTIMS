from flask import Blueprint
from flask_login import login_required
from controllers.certificate_controller import CertificateController
from utils.decorators import require_module

certificate_bp = Blueprint('certificate', __name__, url_prefix='/api/certificates')

@certificate_bp.route('/', methods=['GET'])
@login_required
@require_module('certificates')
def list_certificates():
    """List all certificates with filters"""
    return CertificateController.list_certificates()

@certificate_bp.route('/stats', methods=['GET'])
@login_required
@require_module('certificates')
def get_certificate_stats():
    """Get certificate statistics"""
    return CertificateController.get_certificate_stats()

@certificate_bp.route('/eligible', methods=['GET'])
@login_required
@require_module('certificates')
def get_eligible_enrollments():
    """Get enrollments eligible for certificate"""
    return CertificateController.get_eligible_enrollments()

@certificate_bp.route('/<int:certificate_id>', methods=['GET'])
@login_required
@require_module('certificates')
def get_certificate(certificate_id):
    """Get certificate details by ID"""
    return CertificateController.get_certificate(certificate_id)

@certificate_bp.route('/verify/<token>', methods=['GET'])
def verify_certificate(token):
    """Verify a certificate by token (public endpoint)"""
    return CertificateController.verify_certificate(token)

@certificate_bp.route('/', methods=['POST'])
@login_required
@require_module('certificates')
def generate_certificate():
    """Generate a new certificate"""
    return CertificateController.generate_certificate()

@certificate_bp.route('/<int:certificate_id>/revoke', methods=['POST'])
@login_required
@require_module('certificates')
def revoke_certificate(certificate_id):
    """Revoke a certificate"""
    return CertificateController.revoke_certificate(certificate_id)
