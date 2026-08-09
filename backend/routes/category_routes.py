from flask import Blueprint, request, jsonify
from flask_login import login_required
from controllers.category_controller import CategoryController
from models import Category, db
from sqlalchemy import or_
from utils.decorators import require_module

category_bp = Blueprint('category', __name__, url_prefix='/api/categories')

@category_bp.route('/', methods=['GET'])
@login_required
@require_module('categories')
def list_categories():
    """List all categories with hierarchy"""
    try:
        search = request.args.get('search', '')
        status = request.args.get('status', '')
        
        query = Category.query
        
        # Apply search filter
        if search:
            query = query.filter(
                or_(
                    Category.category_name.like(f'%{search}%'),
                    Category.category_code.like(f'%{search}%')
                )
            )
        
        # Apply status filter
        if status and status != '':
            query = query.filter(Category.status == status)
        
        # Order by display_order
        categories = query.order_by(Category.display_order).all()
        
        return jsonify({
            'success': True,
            'data': [c.to_dict() for c in categories]
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@category_bp.route('/hierarchy', methods=['GET'])
@login_required
@require_module('categories')
def get_category_hierarchy():
    """Get full category hierarchy"""
    return CategoryController.get_category_hierarchy()

@category_bp.route('/stats', methods=['GET'])
@login_required
@require_module('categories')
def get_category_stats():
    """Get category statistics"""
    return CategoryController.get_category_stats()

@category_bp.route('/<int:category_id>', methods=['GET'])
@login_required
@require_module('categories')
def get_category(category_id):
    """Get category details by ID"""
    return CategoryController.get_category(category_id)

@category_bp.route('/', methods=['POST'])
@login_required
@require_module('categories')
def create_category():
    """Create a new category"""
    return CategoryController.create_category()

@category_bp.route('/reorder', methods=['POST'])
@login_required
@require_module('categories')
def reorder_categories():
    """Bulk reorder categories"""
    return CategoryController.reorder_categories()

@category_bp.route('/<int:category_id>', methods=['PUT'])
@login_required
@require_module('categories')
def update_category(category_id):
    """Update an existing category"""
    return CategoryController.update_category(category_id)

@category_bp.route('/<int:category_id>', methods=['DELETE'])
@login_required
@require_module('categories')
def delete_category(category_id):
    """Delete a category"""
    return CategoryController.delete_category(category_id)
