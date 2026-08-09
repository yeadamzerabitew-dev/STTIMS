from flask import Blueprint, request, jsonify
from flask_login import login_required
from controllers.result_controller import ResultController
from models import GradeScale, db
from utils.decorators import require_module

result_bp = Blueprint('result', __name__, url_prefix='/api/results')

@result_bp.route('/', methods=['GET'])
@login_required
@require_module('results')
def list_results():
    """List all trainee results with filters and pagination"""
    return ResultController.list_results()

@result_bp.route('/', methods=['POST'])
@login_required
@require_module('results')
def create_result():
    """Create a new result"""
    return ResultController.create_result()

@result_bp.route('/bulk', methods=['POST'])
@login_required
@require_module('results')
def bulk_results():
    """Create/update results for multiple trainees"""
    return ResultController.bulk_results()

@result_bp.route('/assessment/<int:assessment_id>', methods=['GET'])
@login_required
@require_module('results')
def get_assessment_results(assessment_id):
    """Get results for a specific assessment"""
    return ResultController.get_assessment_results(assessment_id)

@result_bp.route('/trainee/<int:trainee_id>', methods=['GET'])
@login_required
@require_module('results')
def get_trainee_results(trainee_id):
    """Get results for a specific trainee"""
    return ResultController.get_trainee_results(trainee_id)

@result_bp.route('/verify/<int:result_id>', methods=['POST'])
@login_required
@require_module('results')
def verify_result(result_id):
    """Verify a result"""
    return ResultController.verify_result(result_id)

@result_bp.route('/stats', methods=['GET'])
@login_required
@require_module('results')
def get_result_stats():
    """Get result statistics"""
    return ResultController.get_result_stats()

@result_bp.route('/grade-scale', methods=['GET'])
@login_required
@require_module('results')
def get_grade_scale():
    """Get grade scale"""
    try:
        grades = GradeScale.query.order_by(GradeScale.display_order).all()
        return jsonify({
            'success': True,
            'data': [g.to_dict() for g in grades]
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@result_bp.route('/grade-scale', methods=['POST'])
@login_required
@require_module('results')
def create_grade_scale():
    """Create a new grade scale entry"""
    try:
        data = request.get_json()

        if not data.get('grade_letter') or data.get('min_percentage') is None or data.get('max_percentage') is None:
            return jsonify({'success': False, 'message': 'Grade letter, min and max percentage are required'}), 400

        grade = GradeScale(
            grade_letter=data['grade_letter'],
            grade_point=data.get('grade_point', 0.0),
            min_percentage=data['min_percentage'],
            max_percentage=data['max_percentage'],
            description=data.get('description', ''),
            is_pass=data.get('is_pass', True),
            display_order=data.get('display_order', 0)
        )

        db.session.add(grade)
        db.session.commit()

        return jsonify({
            'success': True,
            'data': grade.to_dict(),
            'message': 'Grade scale created successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@result_bp.route('/grade-scale/<int:grade_id>', methods=['PUT'])
@login_required
@require_module('results')
def update_grade_scale(grade_id):
    """Update a grade scale entry"""
    try:
        grade = GradeScale.query.get(grade_id)
        if not grade:
            return jsonify({'success': False, 'message': 'Grade scale not found'}), 404

        data = request.get_json()

        if 'grade_letter' in data:
            grade.grade_letter = data['grade_letter']
        if 'grade_point' in data:
            grade.grade_point = data['grade_point']
        if 'min_percentage' in data:
            grade.min_percentage = data['min_percentage']
        if 'max_percentage' in data:
            grade.max_percentage = data['max_percentage']
        if 'description' in data:
            grade.description = data['description']
        if 'is_pass' in data:
            grade.is_pass = data['is_pass']
        if 'display_order' in data:
            grade.display_order = data['display_order']

        db.session.commit()

        return jsonify({
            'success': True,
            'data': grade.to_dict(),
            'message': 'Grade scale updated successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@result_bp.route('/grade-scale/<int:grade_id>', methods=['DELETE'])
@login_required
@require_module('results')
def delete_grade_scale(grade_id):
    """Delete a grade scale entry"""
    try:
        grade = GradeScale.query.get(grade_id)
        if not grade:
            return jsonify({'success': False, 'message': 'Grade scale not found'}), 404

        db.session.delete(grade)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Grade scale deleted successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
