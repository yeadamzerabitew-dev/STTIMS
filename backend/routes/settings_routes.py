from flask import Blueprint, jsonify, request
from flask_login import login_required
from models import db, User, Setting
import json
from utils.decorators import require_module

settings_bp = Blueprint('settings', __name__, url_prefix='/api/settings')

@settings_bp.route('/', methods=['GET'])
@login_required
@require_module('settings')
def get_settings():
    """Get system settings"""
    try:
        # Check if settings exist in database
        settings_record = Setting.query.first()
        
        if settings_record:
            # Return settings from database
            return jsonify({
                'success': True,
                'data': settings_record.to_dict()
            })
        
        # Return default settings if no settings in database
        settings = {
            'institution': {
                'name': 'Short-Term Training Institution',
                'code': 'STTI',
                'address': 'Addis Ababa, Ethiopia',
                'phone': '+251-911-234567',
                'email': 'info@sttims.com'
            },
            'theme': 'default',
            'certificate_template': 'professional',
            'email': {
                'smtp_server': 'smtp.gmail.com',
                'smtp_port': 587,
                'address': 'noreply@sttims.com',
                'notifications_enabled': True
            },
            'app_name': 'STTIMS',
            'app_version': '1.0.0'
        }
        return jsonify({
            'success': True,
            'data': settings
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@settings_bp.route('/', methods=['PUT'])
@login_required
@require_module('settings')
def update_settings():
    """Update system settings"""
    try:
        data = request.get_json()
        
        # Check if settings exist
        settings_record = Setting.query.first()
        
        if settings_record:
            # Update existing settings
            if 'institution' in data:
                settings_record.institution_name = data['institution'].get('name', settings_record.institution_name)
                settings_record.institution_code = data['institution'].get('code', settings_record.institution_code)
                settings_record.institution_address = data['institution'].get('address', settings_record.institution_address)
                settings_record.institution_phone = data['institution'].get('phone', settings_record.institution_phone)
                settings_record.institution_email = data['institution'].get('email', settings_record.institution_email)
            
            if 'theme' in data:
                settings_record.theme = data['theme']
            
            if 'certificate_template' in data:
                settings_record.certificate_template = data['certificate_template']
            
            if 'email' in data:
                settings_record.smtp_server = data['email'].get('smtp_server', settings_record.smtp_server)
                settings_record.smtp_port = data['email'].get('smtp_port', settings_record.smtp_port)
                settings_record.email_address = data['email'].get('address', settings_record.email_address)
                settings_record.notifications_enabled = data['email'].get('notifications_enabled', settings_record.notifications_enabled)
            
            db.session.commit()
            
            return jsonify({
                'success': True,
                'data': settings_record.to_dict(),
                'message': 'Settings updated successfully'
            })
        else:
            # Create new settings
            settings = Setting()
            
            # Institution settings
            if 'institution' in data:
                settings.institution_name = data['institution'].get('name', 'Short-Term Training Institution')
                settings.institution_code = data['institution'].get('code', 'STTI')
                settings.institution_address = data['institution'].get('address', 'Addis Ababa, Ethiopia')
                settings.institution_phone = data['institution'].get('phone', '+251-911-234567')
                settings.institution_email = data['institution'].get('email', 'info@sttims.com')
            
            # Theme settings
            settings.theme = data.get('theme', 'default')
            settings.certificate_template = data.get('certificate_template', 'professional')
            
            # Email settings
            if 'email' in data:
                settings.smtp_server = data['email'].get('smtp_server', 'smtp.gmail.com')
                settings.smtp_port = data['email'].get('smtp_port', 587)
                settings.email_address = data['email'].get('address', 'noreply@sttims.com')
                settings.notifications_enabled = data['email'].get('notifications_enabled', True)
            
            db.session.add(settings)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'data': settings.to_dict(),
                'message': 'Settings created successfully'
            })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@settings_bp.route('/institution', methods=['PUT'])
@login_required
@require_module('settings')
def update_institution_settings():
    """Update institution settings only"""
    try:
        data = request.get_json()
        settings_record = Setting.query.first()
        
        if not settings_record:
            settings_record = Setting()
            db.session.add(settings_record)
        
        if 'name' in data:
            settings_record.institution_name = data['name']
        if 'code' in data:
            settings_record.institution_code = data['code']
        if 'address' in data:
            settings_record.institution_address = data['address']
        if 'phone' in data:
            settings_record.institution_phone = data['phone']
        if 'email' in data:
            settings_record.institution_email = data['email']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': settings_record.to_dict(),
            'message': 'Institution settings updated successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@settings_bp.route('/theme', methods=['PUT'])
@login_required
@require_module('settings')
def update_theme():
    """Update theme settings"""
    try:
        data = request.get_json()
        theme = data.get('theme', 'default')
        
        settings_record = Setting.query.first()
        if not settings_record:
            settings_record = Setting()
            db.session.add(settings_record)
        
        settings_record.theme = theme
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': {'theme': theme},
            'message': 'Theme updated successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@settings_bp.route('/email', methods=['PUT'])
@login_required
@require_module('settings')
def update_email_settings():
    """Update email settings"""
    try:
        data = request.get_json()
        settings_record = Setting.query.first()
        
        if not settings_record:
            settings_record = Setting()
            db.session.add(settings_record)
        
        if 'smtp_server' in data:
            settings_record.smtp_server = data['smtp_server']
        if 'smtp_port' in data:
            settings_record.smtp_port = data['smtp_port']
        if 'address' in data:
            settings_record.email_address = data['address']
        if 'password' in data and data['password']:
            settings_record.email_password = data['password']
        if 'notifications_enabled' in data:
            settings_record.notifications_enabled = data['notifications_enabled']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': settings_record.to_dict(),
            'message': 'Email settings updated successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@settings_bp.route('/certificate-template', methods=['PUT'])
@login_required
@require_module('settings')
def update_certificate_template():
    """Update certificate template settings"""
    try:
        data = request.get_json()
        template = data.get('template', 'professional')
        
        settings_record = Setting.query.first()
        if not settings_record:
            settings_record = Setting()
            db.session.add(settings_record)
        
        settings_record.certificate_template = template
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': {'certificate_template': template},
            'message': 'Certificate template updated successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@settings_bp.route('/logo', methods=['POST'])
@login_required
@require_module('settings')
def upload_logo():
    """Upload institution logo"""
    try:
        if 'logo' not in request.files:
            return jsonify({'success': False, 'message': 'No logo file provided'}), 400
        
        file = request.files['logo']
        if file.filename == '':
            return jsonify({'success': False, 'message': 'No file selected'}), 400
        
        # Save file logic here
        # For now, return success
        return jsonify({
            'success': True,
            'data': {'logo_url': '/static/uploads/logo.png'},
            'message': 'Logo uploaded successfully'
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@settings_bp.route('/logo', methods=['DELETE'])
@login_required
@require_module('settings')
def remove_logo():
    """Remove institution logo"""
    try:
        # Remove logo logic here
        return jsonify({
            'success': True,
            'message': 'Logo removed successfully'
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@settings_bp.route('/system-info', methods=['GET'])
@login_required
@require_module('settings')
def get_system_info():
    """Get system information"""
    try:
        import os
        import sys
        import platform
        
        return jsonify({
            'success': True,
            'data': {
                'app_name': 'STTIMS',
                'app_version': '1.0.0',
                'python_version': sys.version,
                'platform': platform.platform(),
                'os': platform.system(),
                'os_version': platform.release(),
                'server_time': datetime.now().isoformat()
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@settings_bp.route('/clear-cache', methods=['POST'])
@login_required
@require_module('settings')
def clear_cache():
    """Clear system cache"""
    try:
        # Clear cache logic here
        return jsonify({
            'success': True,
            'message': 'Cache cleared successfully'
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
